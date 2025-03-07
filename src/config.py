from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg2://postgres:123@db:5432/postgres"  # "postgresql+psycopg2://postgres:123@localhost:5432/postgres"
    DB_HOST: str = ""
    DB_PORT: int = 0
    CONTAINER_DB_PORT: int = 0
    HOST_DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
