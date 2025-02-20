import pandas as pd
from typing import Dict, Any
import json
from .exceptions import DataConversionError
from .logger import logger


class ParquetConverter:
    @staticmethod
    def convert_message_to_parquet(message: list) -> bytes:
        try:
            df = pd.DataFrame(message)
            parquet_buffer = df.to_parquet()
            logger.info("Message successfully converted to parquet format")
            return parquet_buffer
        except Exception as e:
            logger.error(f"Failed to convert message to parquet: {str(e)}")
            raise DataConversionError(f"Failed to convert message to parquet: {str(e)}")
