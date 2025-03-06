import json
import time
import pytest
from unittest.mock import MagicMock, patch
from data_ingestion.data_processor import DataProcessor
from data_ingestion.storage import SupabaseStorage
from data_ingestion.parquet_converter import ParquetConverter

@pytest.fixture
def mock_storage():
    return MagicMock(spec=SupabaseStorage)

@pytest.fixture
def mock_processor(mock_storage):
    return DataProcessor(storage=mock_storage)

@pytest.fixture
def mock_channel():
    return MagicMock()

@pytest.fixture
def mock_method():
    return MagicMock(delivery_tag=123)

@pytest.fixture
def mock_properties():
    return MagicMock()

@patch("data_ingestion.parquet_converter.ParquetConverter.convert_message_to_parquet")
def test_process_message_success(mock_convert, mock_processor, mock_storage, mock_channel, mock_method, mock_properties):
    mock_convert.return_value = b"mock_parquet_data"
    message = [{"id": 1, "name": "Test"}]
    body = json.dumps(message).encode("utf-8")

    with patch("time.time", return_value=1234567890):
        mock_processor.process_message(message)

    mock_convert.assert_called_once_with(message)
    mock_storage.upload_parquet.assert_called_once_with(b"mock_parquet_data", "data_1234567890_1.parquet")


def test_process_message_failure(mock_processor, mock_storage, mock_channel, mock_method, mock_properties):
    body = b"invalid_json"
    
    with pytest.raises(Exception):
        mock_processor.process_message(body)
    
    mock_storage.upload_parquet.assert_not_called()
