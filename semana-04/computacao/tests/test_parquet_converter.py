import pytest
from data_ingestion.parquet_converter import ParquetConverter
from data_ingestion.exceptions import DataConversionError
import pandas as pd
from io import BytesIO


def test_convert_message_to_parquet_with_list():
    message = [{"column1": "value1", "column2": "value2"}, {"column1": "value3", "column2": "value4"}]
    parquet_buffer = ParquetConverter.convert_message_to_parquet(message)
    df = pd.read_parquet(BytesIO(parquet_buffer))
    assert df.shape == (2, 2)
    assert "column1" in df.columns
    assert "column2" in df.columns


def test_convert_message_to_parquet_with_dict():
    message = {"column1": "value1", "column2": "value2"}
    parquet_buffer = ParquetConverter.convert_message_to_parquet(message)
    df = pd.read_parquet(BytesIO(parquet_buffer))
    assert df.shape == (1, 2)
    assert "column1" in df.columns
    assert "column2" in df.columns


def test_convert_message_to_parquet_with_invalid_format():
    message = "Invalid message format"
    with pytest.raises(DataConversionError):
        ParquetConverter.convert_message_to_parquet(message)
