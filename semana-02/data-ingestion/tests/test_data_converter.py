import pytest
from data_ingestion.data_converter import ParquetConverter
from data_ingestion.exceptions import DataConversionError

def test_convert_message_to_parquet_success(sample_message):
    result = ParquetConverter.convert_message_to_parquet(sample_message)
    assert isinstance(result, bytes)
    
    df = pd.read_parquet(pd.io.common.BytesIO(result))
    assert len(df) == 1
    assert df.iloc[0]['id'] == sample_message['id']

def test_convert_message_to_parquet_invalid_input():
    with pytest.raises(DataConversionError):
        ParquetConverter.convert_message_to_parquet(None)

def test_convert_message_to_parquet_empty_dict():
    result = ParquetConverter.convert_message_to_parquet({})
    assert isinstance(result, bytes)

def test_convert_message_to_parquet_nested_dict(sample_message):
    nested_message = {
        **sample_message,
        "nested": {"key": "value"}
    }
    result = ParquetConverter.convert_message_to_parquet(nested_message)
    assert isinstance(result, bytes)