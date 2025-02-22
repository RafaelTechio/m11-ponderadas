import pytest
from unittest.mock import MagicMock, patch
import json
import pandas as pd
import pika

@pytest.fixture
def sample_message():
    return {
        "id": 123,
        "timestamp": "2024-02-21T10:00:00",
        "data": "test data",
        "value": 42.0
    }

@pytest.fixture
def mock_channel():
    channel = MagicMock()
    channel.basic_ack = MagicMock()
    channel.basic_nack = MagicMock()
    return channel

@pytest.fixture
def mock_pika_connection():
    with patch('pika.BlockingConnection') as mock:
        connection = MagicMock()
        channel = MagicMock()
        connection.channel.return_value = channel
        mock.return_value = connection
        yield mock

@pytest.fixture
def mock_supabase():
    with patch('supabase.create_client') as mock:
        client = MagicMock()
        storage = MagicMock()
        client.storage.from_.return_value = storage
        mock.return_value = client
        yield mock