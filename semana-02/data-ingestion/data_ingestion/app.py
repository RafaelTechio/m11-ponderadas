import signal
import sys
import time
import json
from data_ingestion.queue_consumer import RabbitMQConsumer
from data_ingestion.storage import SupabaseStorage
from data_ingestion.config import Config
from data_ingestion.logger import logger
from data_ingestion.data_processor import DataProcessor
from data_ingestion.dlq_handler import DLQHandler

class App:
    def __init__(self, config: Config):
        self.consumer = RabbitMQConsumer(
            host=config.RABBITMQ_HOST,
            queue=config.RABBITMQ_QUEUE,
            port=config.RABBITMQ_PORT,
            user=config.RABBITMQ_USERNAME,
            password=config.RABBITMQ_PASSWORD,
        )

        self.storage = SupabaseStorage(
            url=config.SUPABASE_URL,
            key=config.SUPABASE_KEY,
            bucket=config.SUPABASE_BUCKET,
        )

        self.dlq_handler = DLQHandler(config.RABBITMQ_DLQ, self.consumer)
        self.processor = DataProcessor(self.storage)

        self.message_retry_number: int = config.MESSAGE_RETRY_NUMBER
        self.setup_signal_handlers()

    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def handle_shutdown(self, signum, frame):
        logger.info("Recebido sinal de desligamento. Encerrando graciosamente...")
        self.consumer.close()
        sys.exit(0)

    def handle_message_failure(self, ch, method, message):
        self.dlq_handler.move_to_dlq(message)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def process_message_with_retries(self, ch, method, properties, message):
        for attempt in range(self.message_retry_number):
            try:
                if isinstance(message, bytes):
                    message = message.decode("utf-8")
                message = json.loads(message)

                self.processor.process_message(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return True
            except Exception as e:
                logger.error(f"Erro na tentativa {attempt + 1} ao processar a mensagem: {str(e)}")
                time.sleep(1)

        self.handle_message_failure(ch, method, message)
        return False

    def run(self):
        while True:
            try:
                logger.info("Iniciando aplicação de ingestão de dados...")
                self.consumer.connect()

                while True:
                    try:
                        self.consumer.consume(self.process_message_with_retries)

                    except Exception as e:
                        logger.error(f"Erro ao consumir mensagem: {str(e)}")
                        continue

            except Exception as e:
                logger.error(f"Erro na execução da aplicação: {str(e)}")
                sys.exit(1)
