from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    database_url: str = "postgresql+psycopg2://postgres:sebas@localhost/db_cepas"
    secret_key: SecretStr = SecretStr("secret123")
    debug = True
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
