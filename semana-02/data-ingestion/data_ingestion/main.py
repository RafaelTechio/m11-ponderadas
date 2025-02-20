import json
import signal
import sys
from data_ingestion.queue_consumer import RabbitMQConsumer
from data_ingestion.data_converter import ParquetConverter
from data_ingestion.storage import SupabaseStorage
from data_ingestion.config import Config
from data_ingestion.logger import logger
import time

class DataIngestionApp:
    def __init__(self):
        self.consumer = RabbitMQConsumer(
            host=Config.RABBITMQ_HOST,
            queue=Config.RABBITMQ_QUEUE,
            port=Config.RABBITMQ_PORT,
            user=Config.RABBITMQ_USERNAME,
            password=Config.RABBITMQ_PASSWORD,
        )

        self.storage = SupabaseStorage(
            url=Config.SUPABASE_URL,
            key=Config.SUPABASE_KEY,
            bucket=Config.SUPABASE_BUCKET,
        )

        self.setup_signal_handlers()

    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def handle_shutdown(self, signum, frame):
        logger.info("Recebido sinal de desligamento. Encerrando graciosamente...")
        self.consumer.close()
        sys.exit(0)

    def process_message(self, ch, method, properties, body):
        try:
            # Decodifica a mensagem
            message: list = json.loads(body)

            logger.info(f"Mensagem recebida: {len(message)} linhas")

            # Converte para parquet
            parquet_data = ParquetConverter.convert_message_to_parquet(message)

            # Upload para Supabase
            file_name = f"data_{time.time()}_{len(message)}.parquet"
            self.storage.upload_parquet(parquet_data, file_name)

            # Confirma o processamento
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Mensagem processada com sucesso: {file_name}")

        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            # Rejeita a mensagem em caso de erro
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def run(self):
        try:
            logger.info("Iniciando aplicação de ingestão de dados...")
            self.consumer.connect()
            self.consumer.consume(self.process_message)
        except Exception as e:
            logger.error(f"Erro na execução da aplicação: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    app = DataIngestionApp()
    app.run()
