import pytest
from data_ingestion.main import DataIngestionApp
from unittest.mock import patch, MagicMock

@pytest.fixture
def app(mock_pika_connection, mock_supabase):
    with patch('data_ingestion.main.Config') as mock_config:
        mock_config.RABBITMQ_HOST = "localhost"
        mock_config.RABBITMQ_QUEUE = "test_queue"
        mock_config.RABBITMQ_PORT = 5672
        mock_config.SUPABASE_URL = "test_url"
        mock_config.SUPABASE_KEY = "test_key"
        mock_config.SUPABASE_BUCKET = "test_bucket"
        return DataIngestionApp()

def test_app_initialization(app):
    assert app.consumer is not None
    assert app.storage is not None

def test_process_message_success(app, mock_channel, sample_message):
    app.process_message(
        mock_channel,
        MagicMock(),
        None,
        json.dumps(sample_message).encode()
    )
    mock_channel.basic_ack.assert_called_once()

def test_process_message_failure(app, mock_channel):
    app.process_message(
        mock_channel,
        MagicMock(),
        None,
        b"invalid json"
    )
    mock_channel.basic_nack.assert_called_once()

def test_run_success(app):
    with patch.object(app.consumer, 'connect') as mock_connect:
        with patch.object(app.consumer, 'consume') as mock_consume:
            app.run()
            mock_connect.assert_called_once()
            mock_consume.assert_called_once()

def test_run_failure(app):
    with patch.object(app.consumer, 'connect', side_effect=Exception("Connection failed")):
        with pytest.raises(SystemExit):
            app.run()