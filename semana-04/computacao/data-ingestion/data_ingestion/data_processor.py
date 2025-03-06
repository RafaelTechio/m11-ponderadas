import json
import time
from data_ingestion.parquet_converter import ParquetConverter
from data_ingestion.storage import SupabaseStorage
from data_ingestion.logger import logger

class DataProcessor:
    def __init__(self, storage: SupabaseStorage):
        self.storage = storage

    def process_message(self, message: list):
        try:
            logger.info("Oi")
            logger.info(f"Mensagem recebida: {len(message)} linhas")
            parquet_data = ParquetConverter.convert_message_to_parquet(message)
            file_name = f"data_{time.time()}_{len(message)}.parquet"
            self.storage.upload_parquet(parquet_data, file_name)
            logger.info(f"Mensagem processada com sucesso: {file_name}")
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            raise e
