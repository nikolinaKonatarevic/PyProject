from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.api.config import settings

sync_engine = create_engine(settings.postgres_dsn.unicode_string())

session_factory = sessionmaker(autoflush=False, autocommit=False, bind=sync_engine)


def get_db_session() -> Session:
    """
    Dependency that provides a session to interact with the database.
    """
    with session_factory() as session:
        yield session


def get_sync_engine():
    return sync_engine
