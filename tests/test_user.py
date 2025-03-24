from starlette import status
from starlette.testclient import TestClient

from src.api.users import dto
from src.api.users.models import User


# CREATE
def test_create_user(
    client: TestClient,
    create_test_user: User,
    create_test_token: str,
) -> None:
    data = {"email": "email", "password": "default_password", "repeat_password": "default_password"}

    result = client.post("/v1/users/auth", json=data)

    assert result.json()["email"] == data["email"] and result.json()["password_hashed"]
    assert result.status_code == status.HTTP_201_CREATED


# LOGIN
def test_login(
    client: TestClient,
    create_test_user: User,
    create_test_token: str,
) -> None:
    data = {"email": "email", "password": "default_password"}

    result = client.post("/v1/users/login", json=data)

    assert result.status_code == status.HTTP_200_OK
