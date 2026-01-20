from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Пути
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    STORAGE_DIR: Path = BASE_DIR / "storage"

    # БД (подставятся из .env, если там есть такие ключи)
    #DB_HOST: str = "localhost"
    #DB_PORT: int = 5432
    #DATABASE_URL: str

    # API Keys
    #PEXELS_API_KEY: str
    
    APP_HOST: str = '127.0.0.1'
    APP_PORT: int = 8000
    
    DEBUG: bool = False
    
    # Автоматическое чтение из .env файла
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
