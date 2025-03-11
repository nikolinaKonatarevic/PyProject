from datetime import timedelta
from typing import Callable, Generator

import pytest
from fastapi import Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from src.auth.auth import create_access_token
from src.config import settings
from src.database.base_model import Base
from src.deps import get_project_service, get_user_service
from src.main import app
from src.projects import project_dto
from src.projects.services import ProjectService
from src.users import dto
from src.users.services import UserService

test_engine = create_engine(settings.postgres_dsn.unicode_string())

test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def test_get_db_session():
    with test_session_factory() as test_session:
        yield test_session


# ERROR!tests/conftest.py:13: error: Module "src.database.sync_engine" has no attribute "get_db_session"  [attr-defined]
# app.dependency_overrides[get_db_session] = test_get_db_session


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
def test_projects(
    test_user: dto.User, project_services: ProjectService = Depends(get_project_service)
) -> list[project_dto.Project]:
    projects = [project_dto.ProjectCreate(name=f"project{i}", description=f"Description{i}") for i in range(3)]
    return [project_services.create_project(project, test_user) for project in projects]


@pytest.fixture
def user_factory() -> Callable[..., dto.User]:
    def _create_test_user(email: str, user_service: UserService = Depends(get_user_service)) -> dto.User:
        user = dto.UserCreate(email=email, password="12345678", repeat_password="12345678")
        return user_service.create_user(user)

    # ERROR ! AttributeError: 'Depends' object has no attribute 'execute'

    return _create_test_user


@pytest.fixture(scope="function")
def test_user(user_factory: Callable[..., dto.User]) -> dto.User:
    return user_factory("test")


@pytest.fixture(scope="function")
def unauthorized_user(user_factory: Callable[..., dto.User]) -> dto.User:
    return user_factory("unauthorized")


@pytest.fixture(scope="function")
def invited_user(user_factory: Callable[..., dto.User]) -> dto.User:
    return user_factory("invited")


@pytest.fixture
def participant_user(user_factory: Callable[..., dto.User]) -> dto.User:
    return user_factory("participant")


# to add mock data for documents


# Creating tokens
@pytest.fixture
def token_factory() -> Callable[..., str]:
    def _create_token(user: dto.User) -> str:
        token_expires = timedelta(minutes=60)
        token = create_access_token(
            data={"email": user.email, "id": str(user.id)},
            expires_delta=token_expires,
        )
        return token

    return _create_token


@pytest.fixture(scope="function")
def test_token(token_factory: Callable[..., str], test_user: dto.User) -> str:
    return token_factory(test_user)


@pytest.fixture(scope="function")
def unauthorized_token(token_factory: Callable[..., str], unauthorized_user: dto.User) -> str:
    return token_factory(unauthorized_user)


@pytest.fixture
def participant_token(token_factory: Callable[..., str], participant_user: dto.User) -> str:
    return token_factory(participant_user)
