from typing import Callable, Optional
import pika
from .exceptions import QueueConnectionError, MessageProcessingError
from .logger import logger

class RabbitMQConsumer:
    def __init__(self, host: str, queue: str, user: str, password: str, port: int = 5672):
        self.host = host
        self.queue = queue
        self.port = port
        self.user = user
        self.password = password
        self._connection = None
        self._channel = None

    def connect(self) -> None:
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=pika.PlainCredentials(self.user, self.password),
                )
            )
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self.queue, durable=True)
            logger.info(f"Connected to RabbitMQ queue: {self.queue}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise QueueConnectionError(f"Failed to connect to RabbitMQ: {str(e)}")

    def consume(self, callback: Callable) -> None:
        try:
            self._channel.basic_consume(
                queue=self.queue, on_message_callback=callback, auto_ack=False
            )
            logger.info("Starting to consume messages...")
            self._channel.start_consuming()
        except Exception as e:
            logger.error(f"Error consuming messages: {str(e)}")
            raise MessageProcessingError(f"Error consuming messages: {str(e)}")

    def publish(self, queue: str, message: str) -> None:
        try:
            self._channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            logger.info(f"Message sent to {queue}: {message}")
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
            raise QueueConnectionError(f"Error publishing message: {str(e)}")

    def close(self) -> None:
        if self._connection:
            self._connection.close()
            logger.info("Connection closed")