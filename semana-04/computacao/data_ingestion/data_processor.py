import json
import time
from data_ingestion.parquet_converter import ParquetConverter
from data_ingestion.storage import SupabaseStorage
from data_ingestion.metrics import MetricsPrometheus
from data_ingestion.logger import logger

class DataProcessor:
    def __init__(self, storage: SupabaseStorage, metrics: MetricsPrometheus):
        self.storage = storage
        self.metrics = metrics

    def process_message(self, message: list):
        with self.metrics.request_duration.time():
            try:
                self.metrics.REQUEST_COUNT.inc()
                logger.info(f"Mensagem recebida: {len(message)} linhas")
                parquet_data = ParquetConverter.convert_message_to_parquet(message)
                file_name = f"data_{time.time()}_{len(message)}.parquet"
                self.storage.upload_parquet(parquet_data, file_name)
                self.metrics.supabase_storage_accesses.inc()
                logger.info(f"Mensagem processada com sucesso: {file_name}")
            except Exception as e:
                logger.error(f"Erro ao processar mensagem: {str(e)}")
                raise e
