from functools import lru_cache

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 0
    CONTAINER_DB_PORT: int = 0
    HOST_DB_PORT: int = 0
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    AWS_BUCKET_NAME: str
    AWS_DEFAULT_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    postgres_dsn: PostgresDsn | None = None  # type = ignore

    @field_validator("postgres_dsn", mode="before")  # noqa
    @classmethod
    def get_postgres_dsn(cls, _, info: ValidationInfo):
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=info.data["DB_USER"],
            password=info.data["DB_PASSWORD"],
            host=info.data["DB_HOST"],
            port=info.data["CONTAINER_DB_PORT"],
            path=info.data["DB_NAME"],
        ).unicode_string()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
