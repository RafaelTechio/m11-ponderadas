import pytest
from data_ingestion.config import Config
from data_ingestion.exceptions import ConfigError

def test_config_with_valid_object():
    mock_env = {
        "RABBITMQ_HOST": "test_host",
        "RABBITMQ_PORT": "1234",
        "RABBITMQ_QUEUE": "test_queue",
        "RABBITMQ_DLQ": "test_queue_dlq",
        "RABBITMQ_USERNAME": "test_user",
        "RABBITMQ_PASSWORD": "test_pass",
        "MESSAGE_RETRY_NUMBER": "3",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_KEY": "test_key",
        "SUPABASE_BUCKET": "test_bucket"
    }

    config = Config(mock_env)

    assert isinstance(config.RABBITMQ_HOST, str)
    assert isinstance(config.RABBITMQ_PORT, int)
    assert isinstance(config.RABBITMQ_QUEUE, str)
    assert isinstance(config.RABBITMQ_DLQ, str)
    assert isinstance(config.RABBITMQ_USERNAME, str)
    assert isinstance(config.RABBITMQ_PASSWORD, str)
    assert isinstance(config.SUPABASE_URL, str)
    assert isinstance(config.SUPABASE_KEY, str)
    assert isinstance(config.SUPABASE_BUCKET, str)

def test_config_with_missing_required_variable():
    mock_env = {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_QUEUE": "data_queue",
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    }

    with pytest.raises(ConfigError):
        Config(mock_env)

def test_config_with_invalid_port_type():
    mock_env = {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "invalid_port",
        "RABBITMQ_QUEUE": "data_queue",
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    }

    with pytest.raises(ConfigError):
        Config(mock_env)

def test_config_with_empty_object():
     mock_env = {}

     with pytest.raises(ConfigError):
         Config(mock_env)
