import pytest
from data_ingestion.storage import SupabaseStorage
from data_ingestion.exceptions import StorageError

def test_supabase_init():
    storage = SupabaseStorage(url="test_url", key="test_key", bucket="test_bucket")
    assert storage.bucket == "test_bucket"

def test_upload_parquet_success(mock_supabase, sample_message):
    storage = SupabaseStorage(url="test_url", key="test_key", bucket="test_bucket")
    
    parquet_data = b"fake parquet data"
    file_name = "test.parquet"
    
    storage.upload_parquet(parquet_data, file_name)
    
    storage.client.storage.from_.assert_called_once_with("test_bucket")
    storage.client.storage.from_().upload.assert_called_once_with(
        path=file_name,
        file=parquet_data,
        file_options={"content-type": "application/parquet"}
    )

def test_upload_parquet_failure(mock_supabase):
    storage = SupabaseStorage(url="test_url", key="test_key", bucket="test_bucket")
    
    # Configura o mock para lançar uma exceção
    storage.client.storage.from_().upload.side_effect = Exception("Upload failed")
    
    with pytest.raises(StorageError):
        storage.upload_parquet(b"data", "test.parquet")
