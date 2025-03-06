import pytest
from unittest.mock import Mock, patch, call
import json
import signal

from data_ingestion.queue_consumer import RabbitMQConsumer
from data_ingestion.storage import SupabaseStorage
from data_ingestion.config import Config
from data_ingestion.data_processor import DataProcessor
from data_ingestion.dlq_handler import DLQHandler
from data_ingestion.app import App

@pytest.fixture
def mock_config():
    config = Mock(spec=Config)
    config.RABBITMQ_HOST = "localhost"
    config.RABBITMQ_QUEUE = "test_queue"
    config.RABBITMQ_PORT = 5672
    config.RABBITMQ_USERNAME = "guest"
    config.RABBITMQ_PASSWORD = "guest"
    config.SUPABASE_URL = "http://test"
    config.SUPABASE_KEY = "test_key"
    config.SUPABASE_BUCKET = "test_bucket"
    config.RABBITMQ_DLQ = "test_dlq"
    config.MESSAGE_RETRY_NUMBER = 3
    return config

@pytest.fixture
def mock_consumer():
    return Mock(spec=RabbitMQConsumer)

@pytest.fixture
def mock_storage():
    return Mock(spec=SupabaseStorage)

@pytest.fixture
def mock_processor():
    return Mock(spec=DataProcessor)

@pytest.fixture
def mock_dlq_handler():
    return Mock(spec=DLQHandler)

@pytest.fixture
def app(mock_config, mock_consumer, mock_storage, mock_processor, mock_dlq_handler):
    with patch('data_ingestion.app.RabbitMQConsumer') as consumer_mock, \
         patch('data_ingestion.app.SupabaseStorage') as storage_mock, \
         patch('data_ingestion.app.DataProcessor') as processor_mock, \
         patch('data_ingestion.app.DLQHandler') as dlq_handler_mock:
        
        consumer_mock.return_value = mock_consumer
        storage_mock.return_value = mock_storage
        processor_mock.return_value = mock_processor
        dlq_handler_mock.return_value = mock_dlq_handler
        
        return App(mock_config)

def test_app_initialization(app, mock_config):
    assert app.message_retry_number == mock_config.MESSAGE_RETRY_NUMBER
    assert isinstance(app.consumer, RabbitMQConsumer)
    assert isinstance(app.storage, SupabaseStorage)
    assert isinstance(app.processor, DataProcessor)
    assert isinstance(app.dlq_handler, DLQHandler)

def test_signal_handlers_setup(app):
    assert signal.getsignal(signal.SIGINT) == app.handle_shutdown
    assert signal.getsignal(signal.SIGTERM) == app.handle_shutdown

def test_handle_shutdown(app):
    with pytest.raises(SystemExit) as exc_info:
        app.handle_shutdown(signal.SIGTERM, None)
    assert exc_info.value.code == 0
    app.consumer.close.assert_called_once()

def test_handle_message_failure(app):
    ch = Mock()
    method = Mock()
    method.delivery_tag = "test_tag"
    message = "test_message"
    
    app.handle_message_failure(ch, method, message)
    
    app.dlq_handler.move_to_dlq.assert_called_once_with(message)
    ch.basic_nack.assert_called_once_with(delivery_tag="test_tag", requeue=False)

def test_process_message_with_retries_success(app):
    ch = Mock()
    method = Mock()
    method.delivery_tag = "test_tag"
    properties = Mock()
    message = json.dumps({"test": "data"}).encode()
    
    result = app.process_message_with_retries(ch, method, properties, message)
    
    assert result is True
    app.processor.process_message.assert_called_once_with({"test": "data"})
    ch.basic_ack.assert_called_once_with(delivery_tag="test_tag")

def test_process_message_with_retries_failure(app):
    ch = Mock()
    method = Mock()
    method.delivery_tag = "test_tag"
    properties = Mock()
    message = json.dumps({"test": "data"}).encode()
    
    app.processor.process_message.side_effect = Exception("Test error")
    
    with patch('time.sleep'):
        result = app.process_message_with_retries(ch, method, properties, message)
    
    assert result is False

def test_process_message_with_retries_success_after_retry(app):
    ch = Mock()
    method = Mock()
    method.delivery_tag = "test_tag"
    properties = Mock()
    message = json.dumps({"test": "data"}).encode()
    
    test_data = {"test": "data"}
    app.processor.process_message.side_effect = [
        Exception("First try"),
        Exception("Second try"),
        None
    ]
    
    with patch('time.sleep'):
        result = app.process_message_with_retries(ch, method, properties, message)
    
    assert result is False

def test_run_successful_execution(app):
    app.consumer.consume.side_effect = KeyboardInterrupt()
    
    with pytest.raises(KeyboardInterrupt):
        app.run()
    
    app.consumer.connect.assert_called_once()
    app.consumer.consume.assert_called_once_with(app.process_message_with_retries)

def test_run_with_consumer_error(app):
    app.consumer.consume.side_effect = [
        Exception("First error"),
        KeyboardInterrupt()
    ]
    
    with pytest.raises(KeyboardInterrupt):
        app.run()
    
    assert app.consumer.consume.call_count == 2

def test_run_with_connection_error(app):
    app.consumer.connect.side_effect = Exception("Connection error")
    
    with pytest.raises(SystemExit) as exc_info:
        app.run()
    
    assert exc_info.value.code == 1
    app.consumer.connect.assert_called_once()