# storage.py
from supabase import create_client
from typing import Union, BinaryIO  # Corrigindo a importação
from .exceptions import StorageError
from .logger import logger


class SupabaseStorage:
    def __init__(self, url: str, key: str, bucket: str):
        self.client = create_client(url, key)
        self.bucket = bucket

    def upload_parquet(self, data: Union[bytes, BinaryIO], file_name: str) -> str:
        try:
            response = self.client.storage.from_(self.bucket).upload(
                path=file_name,
                file=data,
                file_options={"content-type": "application/parquet"},
            )
            logger.info(f"File {file_name} uploaded successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to upload file to Supabase: {str(e)}")
            raise StorageError(f"Failed to upload file to Supabase: {str(e)}")
