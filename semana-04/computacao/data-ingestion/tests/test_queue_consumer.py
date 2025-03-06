import pytest
import pika
from unittest.mock import MagicMock, patch
from data_ingestion.queue_consumer import RabbitMQConsumer
from data_ingestion.exceptions import QueueConnectionError, MessageProcessingError


@pytest.fixture
def mock_channel():
    return MagicMock()


@pytest.fixture
def mock_connection(mock_channel):
    mock_connection = MagicMock()
    mock_connection.channel.return_value = mock_channel
    return mock_connection


@patch('data_ingestion.queue_consumer.pika.BlockingConnection')
def test_connect_success(mock_blocking_connection, mock_connection, mock_channel):
    mock_blocking_connection.return_value = mock_connection

    consumer = RabbitMQConsumer(
        host="localhost", queue="test_queue", user="user", password="password"
    )
    consumer.connect()

    mock_blocking_connection.assert_called_once_with(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            credentials=pika.PlainCredentials("user", "password"),
        )
    )
    mock_channel.queue_declare.assert_called_once_with(queue="test_queue", durable=True)
    assert consumer._connection == mock_connection
    assert consumer._channel == mock_channel


@patch('data_ingestion.queue_consumer.pika.BlockingConnection')
def test_connect_failure(mock_blocking_connection):
    mock_blocking_connection.side_effect = Exception("Connection failed")

    consumer = RabbitMQConsumer(
        host="localhost", queue="test_queue", user="user", password="password"
    )

    with pytest.raises(QueueConnectionError):
        consumer.connect()


@patch('data_ingestion.queue_consumer.pika.BlockingConnection')
def test_consume_success(mock_blocking_connection, mock_connection, mock_channel):
    mock_blocking_connection.return_value = mock_connection
    consumer = RabbitMQConsumer(
        host="localhost", queue="test_queue", user="user", password="password"
    )
    consumer._channel = mock_channel
    consumer._channel.basic_consume = MagicMock()

    callback = MagicMock()
    consumer.consume(callback)

    mock_channel.basic_consume.assert_called_once_with(
        queue="test_queue", on_message_callback=callback, auto_ack=False
    )
    mock_channel.start_consuming.assert_called_once()


@patch('data_ingestion.queue_consumer.pika.BlockingConnection')
def test_consume_failure(mock_blocking_connection, mock_connection, mock_channel):
    mock_blocking_connection.return_value = mock_connection
    consumer = RabbitMQConsumer(
        host="localhost", queue="test_queue", user="user", password="password"
    )
    consumer._channel = mock_channel
    consumer._channel.basic_consume = MagicMock(side_effect=Exception("Consume failed"))

    callback = MagicMock()
    with pytest.raises(MessageProcessingError):
        consumer.consume(callback)


@patch('data_ingestion.queue_consumer.pika.BlockingConnection')
def test_close(mock_blocking_connection, mock_connection, mock_channel):
    mock_blocking_connection.return_value = mock_connection
    consumer = RabbitMQConsumer(
        host="localhost", queue="test_queue", user="user", password="password"
    )
    consumer._connection = mock_connection
    consumer.close()

    mock_connection.close.assert_called_once()


@patch('data_ingestion.queue_consumer.pika.BlockingConnection')
def test_publish_success(mock_blocking_connection, mock_connection, mock_channel):
    mock_blocking_connection.return_value = mock_connection
    consumer = RabbitMQConsumer(
        host="localhost", queue="test_queue", user="user", password="password"
    )
    consumer._channel = mock_channel

    message = '{"id": 1, "name": "Test Message"}'
    consumer.publish("test_queue", message)

    mock_channel.basic_publish.assert_called_once_with(
        exchange='',
        routing_key="test_queue",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )


@patch('data_ingestion.queue_consumer.pika.BlockingConnection')
def test_publish_failure(mock_blocking_connection, mock_connection, mock_channel):
    mock_blocking_connection.return_value = mock_connection
    consumer = RabbitMQConsumer(
        host="localhost", queue="test_queue", user="user", password="password"
    )
    consumer._channel = mock_channel
    mock_channel.basic_publish = MagicMock(side_effect=Exception("Publish failed"))

    message = '{"id": 1, "name": "Test Message"}'
    with pytest.raises(QueueConnectionError):
        consumer.publish("test_queue", message)

    mock_channel.basic_publish.assert_called_once_with(
        exchange='',
        routing_key="test_queue",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )