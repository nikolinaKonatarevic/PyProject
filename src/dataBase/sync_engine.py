import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

sync_engine = create_engine(os.getenv("DB_URL"))

session_factory = sessionmaker(autoflush=False, autocommit=False, bind=sync_engine)


def get_db_session() -> Session:
    """
    Dependency that provides a session to interact with the database.
    """
    with session_factory() as session:
        try:
            yield session
        finally:
            session.close()
