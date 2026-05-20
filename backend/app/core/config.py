from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
    db_echo: bool = True


settings = Settings()
