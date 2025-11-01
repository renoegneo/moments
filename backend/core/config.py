from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# абсолютный путь к корневой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent  # две папки вверх от текущего файла (core/config.py -> backend/)

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
