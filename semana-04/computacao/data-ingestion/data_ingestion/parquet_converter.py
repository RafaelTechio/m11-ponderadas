import pandas as pd
from .exceptions import DataConversionError
from .logger import logger


class ParquetConverter:
    @staticmethod
    def convert_message_to_parquet(message) -> bytes:
        try:
            if isinstance(message, list):
                df = pd.DataFrame(message)
            elif isinstance(message, dict):
                df = pd.DataFrame([message])
            else:
                raise DataConversionError("Invalid message format. Expected list or dict.")

            parquet_buffer = df.to_parquet()
            logger.info("Message successfully converted to parquet format")
            return parquet_buffer
        except Exception as e:
            logger.error(f"Failed to convert message to parquet: {str(e)}")
            raise DataConversionError(f"Failed to convert message to parquet: {str(e)}")
