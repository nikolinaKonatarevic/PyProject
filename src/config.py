import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg2://postgres:123@localhost:5432/postgres"
    DB_HOST: str = ""
    DB_PORT: int = 0
    CONTAINER_DB_PORT: int = 0
    HOST_DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASSWORD: str = ""

    model_config = SettingsConfigDict(env_file=DOTENV, extra="allow")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
