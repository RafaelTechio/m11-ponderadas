import json
from data_ingestion.logger import logger

class DLQHandler:
    def __init__(self, dlq_queue: str, rabbitmq_consumer):
        self.dlq_queue = dlq_queue
        self.rabbitmq_consumer = rabbitmq_consumer

    def move_to_dlq(self, message):
        try:
            logger.info("Movendo mensagem para a DLQ")
            self.rabbitmq_consumer.publish(self.dlq_queue, message)
            
        except Exception as e:
            logger.error(f"Erro ao mover mensagem para a DLQ: {str(e)}")
            raise e
