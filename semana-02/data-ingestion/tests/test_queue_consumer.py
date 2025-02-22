import pytest
from data_ingestion.queue_consumer import RabbitMQConsumer
from data_ingestion.exceptions import QueueConnectionError, MessageProcessingError

def test_rabbitmq_init():
    consumer = RabbitMQConsumer(host="localhost", queue="test_queue")
    assert consumer.host == "localhost"
    assert consumer.queue == "test_queue"
    assert consumer.port == 5672

def test_rabbitmq_connection_success(mock_pika_connection):
    consumer = RabbitMQConsumer(host="localhost", queue="test_queue")
    consumer.connect()
    
    mock_pika_connection.assert_called_once_with(
        pika.ConnectionParameters(host="localhost", port=5672)
    )
    assert consumer._connection is not None
    assert consumer._channel is not None

def test_rabbitmq_connection_failure(mock_pika_connection):
    mock_pika_connection.side_effect = Exception("Connection failed")
    consumer = RabbitMQConsumer(host="localhost", queue="test_queue")
    
    with pytest.raises(QueueConnectionError):
        consumer.connect()

def test_rabbitmq_consume(mock_pika_connection):
    consumer = RabbitMQConsumer(host="localhost", queue="test_queue")
    consumer.connect()
    
    callback = lambda x: x
    consumer.consume(callback)
    
    consumer._channel.basic_consume.assert_called_once_with(
        queue="test_queue",
        on_message_callback=callback,
        auto_ack=False
    )
    consumer._channel.start_consuming.assert_called_once()

def test_rabbitmq_close(mock_pika_connection):
    consumer = RabbitMQConsumer(host="localhost", queue="test_queue")
    consumer.connect()
    consumer.close()
    
    consumer._connection.close.assert_called_once()