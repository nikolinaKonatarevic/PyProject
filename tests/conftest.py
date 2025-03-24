from datetime import timedelta
from typing import Callable, Generator

import pytest
from sqlalchemy import create_engine, text, Insert, insert
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from src.api.auth.auth import create_access_token, get_password_hash
from src.api.config import settings
from src.api.database.base_model import Base
from src.api.database.sync_engine import get_db_session
from src.api.projects.models import Project
from src.api.users.models import User
from src.main import app

test_engine = create_engine(settings.postgres_dsn.unicode_string())

test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def test_get_db_session():
    with test_session_factory() as test_session:
        yield test_session


# ERROR!tests/conftest.py:13: error: Module "src.database.sync_engine" has no attribute "get_db_session"  [attr-defined]
app.dependency_overrides[get_db_session()] = test_get_db_session


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    session = test_session_factory()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function", autouse=True)
def truncate_tables() -> None:
    with next(test_get_db_session()) as session:
        session.execute(text("SET session_replication_role = replica;"))
    tables_to_truncate = [
        "users",
        "projects",
        "permissions",
        "documents",
    ]
    for table_name in tables_to_truncate:
        session.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))
    session.commit()

    session.execute(text("SET session_replication_role = default;"))


# Creating mock data
@pytest.fixture(scope="function")
def create_test_projects(
    db: Session,
    create_test_user: User
) -> list[Project]:
    projects = [Project(name=f"project{i}", description=f"Description{i}") for i in range(3)]

    query: Insert = (insert(Project).values(projects)
                     .returning(Project))

    result = db.execute(query)
    db.commit()
    data = result.scalars().all()
    return data if data else []


@pytest.fixture(scope="function")
def create_test_user(db: Session) -> User:
    query: Insert = (insert(User).values(email="test@example.com", password_hash= get_password_hash("12345"))
                     .returning(User))

    result = db.execute(query)

    db.commit()
    return result.scalar_one_or_none()

@pytest.fixture(scope="function")
def create_unauthorized_user(db: Session) -> User:
    query: Insert = (insert(User).values(email="unauth@example.com", password_hash=get_password_hash("12345"))
                     .returning(User))

    result = db.execute(query)

    db.commit()
    return result.scalar_one_or_none()

@pytest.fixture(scope="function")
def create_invited_user(db: Session) -> User:
    query: Insert = (insert(User).values(email="invited@example.com", password_hash=get_password_hash("12345"))
                     .returning(User))

    result = db.execute(query)

    db.commit()
    return result.scalar_one_or_none()


@pytest.fixture(scope="function")
def create_participant_user(db: Session) -> User:
    query: Insert = (insert(User).values(email="part@example.com", password_hash=get_password_hash("12345"))
                     .returning(User))

    result = db.execute(query)

    db.commit()
    return result.scalar_one_or_none()


# to add mock data for documents


# Creating tokens
@pytest.fixture
def token_factory() -> Callable[..., str]:
    def _create_token(user: User) -> str:
        token_expires = timedelta(minutes=60)
        token = create_access_token(
            data={"email": user.email, "id": str(user.id)},
            expires_delta=token_expires,
        )
        return token

    return _create_token


@pytest.fixture(scope="function")
def create_test_token(token_factory: Callable[..., str], create_test_user: User) -> str:
    return token_factory(create_test_user)


@pytest.fixture(scope="function")
def create_unauthorized_token(token_factory: Callable[..., str], create_unauthorized_user: User) -> str:
    return token_factory(create_unauthorized_user)


@pytest.fixture
def create_participant_token(token_factory: Callable[..., str], create_participant_user: User) -> str:
    return token_factory(create_participant_user)
