from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from pathlib import Path

# Defining the paths.
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR/'.env', env_file_encoding='utf-8')
    bot_token: SecretStr
    zabbix_username: SecretStr
    zabbix_password: SecretStr

config = Settings()
