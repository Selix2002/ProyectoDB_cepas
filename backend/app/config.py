from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = True
    database_url: str
    secret_key: SecretStr
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
