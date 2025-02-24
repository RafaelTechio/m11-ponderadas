import pytest
from unittest.mock import MagicMock, patch
from data_ingestion.storage import SupabaseStorage
from data_ingestion.exceptions import StorageError


@pytest.fixture
def mock_storage_client():
    mock_client = MagicMock()
    mock_storage = MagicMock()
    mock_storage.from_.return_value = mock_storage
    mock_client.storage.from_.return_value = mock_storage
    return mock_client


@patch('data_ingestion.storage.create_client')
def test_upload_parquet_success(mock_create_client, mock_storage_client):
    mock_create_client.return_value = mock_storage_client

    storage = SupabaseStorage(url="https://supabase.io", key="api_key", bucket="test_bucket")
    mock_response = {"key": "test_key", "url": "https://supabase.io/test_key"}
    mock_storage_client.storage.from_().upload.return_value = mock_response

    file_data = b"fake parquet data"
    file_name = "test.parquet"
    response = storage.upload_parquet(file_data, file_name)

    mock_storage_client.storage.from_().upload.assert_called_once_with(
        path=file_name, file=file_data, file_options={"content-type": "application/parquet"}
    )
    assert response == mock_response


@patch('data_ingestion.storage.create_client')
def test_upload_parquet_failure(mock_create_client, mock_storage_client):
    mock_create_client.return_value = mock_storage_client

    storage = SupabaseStorage(url="https://supabase.io", key="api_key", bucket="test_bucket")
    mock_storage_client.storage.from_().upload.side_effect = Exception("Upload failed")

    file_data = b"fake parquet data"
    file_name = "test.parquet"
    with pytest.raises(StorageError):
        storage.upload_parquet(file_data, file_name)
