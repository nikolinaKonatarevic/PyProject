from starlette.testclient import TestClient

from src.users import dto


# CREATE
def test_create_user(
    client: TestClient,
    test_user: dto.User,
    test_token: str,
) -> None:
    data = {"email": "email", "password": "default_password", "repeat_password": "default_password"}

    result = client.post("/v1/users/auth", json=data)

    assert result.json()["email"] == data["email"] and result.json()["password_hashed"]
    assert result.status_code == 201


# LOGIN
def test_login(
    client: TestClient,
    test_user: dto.User,
    test_token: str,
) -> None:
    data = {"email": "email", "password": "default_password"}

    result = client.post("/v1/users/login", json=data)

    assert result.status_code == 200
