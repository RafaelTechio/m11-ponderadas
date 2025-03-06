from unittest.mock import patch
from data_ingestion.main import main

def test_main():
    with patch("data_ingestion.main.Config") as MockConfig, patch("data_ingestion.main.App") as MockApp:
        mock_app_instance = MockApp.return_value
        main()
        MockConfig.assert_called_once()
        MockApp.assert_called_once_with(MockConfig.return_value)
        mock_app_instance.run.assert_called_once()
