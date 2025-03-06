from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

sync_engine = create_engine(settings.DB_URL)

session_factory = sessionmaker(autoflush=False, autocommit=False, bind=sync_engine)


def get_sync_engine():
    return sync_engine
