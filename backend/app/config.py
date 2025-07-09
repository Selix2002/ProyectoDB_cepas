# backend/app/config.py
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1) carga manual del .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

class Settings(BaseSettings):
    # Ya no necesitas env_file
    model_config = SettingsConfigDict()

    DATABASE_URL: str
    CORS_ORIGINS: list[str] = ["*"]
    FRONTEND_BUILD_DIR: str = str(
        Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
    )
    FRONTEND_MOUNT_PATH: str = "/"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

settings = Settings()
