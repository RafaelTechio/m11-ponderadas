import os
from dotenv import load_dotenv
from data_ingestion.exceptions import ConfigError

class Config:
    def __init__(self, env: dict | None = None):
        try:
            load_dotenv()

            self.env = env if env is not None else os.environ

            self.RABBITMQ_HOST = self._get_var_or_error("RABBITMQ_HOST")
            self.RABBITMQ_PORT = int(self._get_var_or_error("RABBITMQ_PORT"))
            self.RABBITMQ_QUEUE = self._get_var_or_error("RABBITMQ_QUEUE")
            self.RABBITMQ_DLQ = self._get_var_or_error("RABBITMQ_DLQ")
            self.RABBITMQ_USERNAME = self._get_var_or_error("RABBITMQ_USERNAME")
            self.RABBITMQ_PASSWORD = self._get_var_or_error("RABBITMQ_PASSWORD")

            self.MESSAGE_RETRY_NUMBER = int(self._get_var_or_error("MESSAGE_RETRY_NUMBER"))

            self.SUPABASE_URL = self._get_var_or_error("SUPABASE_URL")
            self.SUPABASE_KEY = self._get_var_or_error("SUPABASE_KEY")
            self.SUPABASE_BUCKET = self._get_var_or_error("SUPABASE_BUCKET")
        except ConfigError as e:
            raise e
        except Exception as e:
            raise ConfigError(e)

    def _get_var_or_error(self, var_name: str):
        value = self.env.get(var_name)

        if value is None or value == "":
            raise ConfigError(f"Missing required environment variable: {var_name}")
        return value