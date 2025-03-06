import json
import pytest
from unittest.mock import MagicMock
from data_ingestion.dlq_handler import DLQHandler
from data_ingestion.logger import logger

@pytest.fixture
def mock_rabbitmq_consumer():
    return MagicMock()

@pytest.fixture
def dlq_handler(mock_rabbitmq_consumer):
    return DLQHandler(dlq_queue="dlq_queue", rabbitmq_consumer=mock_rabbitmq_consumer)

def test_move_to_dlq_success(dlq_handler, mock_rabbitmq_consumer):
    message = {"id": 1, "name": "Test Message"}
    
    dlq_handler.move_to_dlq(message)
    
    mock_rabbitmq_consumer.publish.assert_called_once_with("dlq_queue", message)

def test_move_to_dlq_failure(dlq_handler, mock_rabbitmq_consumer):
    message = {"id": 1, "name": "Test Message"}
    mock_rabbitmq_consumer.publish.side_effect = Exception("RabbitMQ error")
    
    with pytest.raises(Exception):
        dlq_handler.move_to_dlq(message)
    
    mock_rabbitmq_consumer.publish.assert_called_once_with("dlq_queue", message)
