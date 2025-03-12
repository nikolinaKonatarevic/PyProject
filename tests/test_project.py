from starlette.testclient import TestClient

from src.projects import project_dto
from src.users import dto


# GET
def test_get_projects(
    client: TestClient,
    test_user: dto.User,
    test_projects: list[project_dto.Project],
    test_token: str,
) -> None:
    result = client.get("/v1/projects", headers={"MyAuthorization": f"Bearer {test_token}"})
    assert result.status_code == 200


def test_get_project(
    client: TestClient,
    test_user: dto.User,
    test_projects: list[project_dto.Project],
    test_token: str,
) -> None:
    test_project = test_projects[0]

    result = client.get(f"/v1/projects/{test_project.id}/info", headers={"MyAuthorization": f"Bearer {test_token}"})

    assert result.json() == {
        "id": str(test_project.id),
        "name": test_project.name,
        "description": test_project.description,
        "owner_id": str(test_project.owner_id),
    }


def test_get_project_unauthorized(
    client: TestClient,
    test_user: dto.User,
    test_projects: list[project_dto.Project],
    unauthorized_token: str,
) -> None:
    test_project = test_projects[0]

    res = client.get(
        f"/v1/projects/{test_project.id}/info",
        headers={"MyAuthorization": f"Bearer {unauthorized_token}"},
    )

    assert res.status_code == 403


def test_get_project_nonexisting(
    client: TestClient,
    test_user: dto.User,
    test_token: str,
) -> None:
    res = client.get(
        "/v1/projects/340002221111/info",
        headers={"MyAuthorization": f"Bearer {test_token}"},
    )

    assert res.status_code == 403


# CREATE
def test_create_project(
    client: TestClient,
    test_user: dto.User,
    test_token: str,
) -> None:
    data = {"name": "project test", "description": "Description for the test project"}

    result = client.post("/v1/projects/", json=data, headers={"MyAuthorization": f"Bearer {test_token}"})

    assert (
        result.json()["name"] == data["name"]
        and result.json()["owner_id"] == str(test_user.id)
        and result.json()["description"] == data["description"]
    )


# UPDATE
def test_update_project(
    client: TestClient,
    test_user: dto.User,
    test_projects: list[project_dto.Project],
    test_token: str,
) -> None:
    test_project = test_projects[0]
    data = {"name": "updated_project", "description": "Updated description"}

    result = client.put(
        f"/v1/projects/{test_project.id}/info",
        json=data,
        headers={"MyAuthorization": f"Bearer {test_token}"},
    )

    assert result.json()["name"] == data["name"] and result.json()["description"] == data["description"]


def test_update_project_nonexisting(
    client: TestClient,
    test_user: dto.User,
    test_token: str,
) -> None:
    data = {"name": "updated_project", "description": "Updated description"}

    result = client.put(
        "/projects/340002221111/info",
        json=data,
        headers={"MyAuthorization": f"Bearer {test_token}"},
    )

    assert result.status_code == 403


# DELETE
def test_delete_project(
    client: TestClient,
    test_user: dto.User,
    test_projects: list[project_dto.Project],
    test_token: str,
) -> None:
    test_project = test_projects[0]

    result = client.delete(f"/v1/projects/{test_project.id}", headers={"MyAuthorization": f"Bearer {test_token}"})

    assert result.status_code == 204


def test_delete_project_nonexisting(
    client: TestClient,
    test_user: dto.User,
    test_token: str,
) -> None:
    result = client.delete(
        "/projects/340002221111/",
        headers={"MyAuthorization": f"Bearer {test_token}"},
    )

    assert result.status_code == 404


def test_delete_project_participant(
    client: TestClient,
    test_user: dto.User,
    test_projects: list[project_dto.Project],
    participant_token: str,
) -> None:
    test_project = test_projects[0]

    result = client.delete(
        f"/v1/projects/{test_project.id}",
        headers={"MyAuthorization": f"Bearer {participant_token}"},
    )

    assert result.status_code == 403


# INVITE
def test_invite_to_project(
    client: TestClient,
    test_user: dto.User,
    test_projects: list[project_dto.Project],
    test_token: str,
    invited_user: dto.User,
) -> None:
    test_project = test_projects[0]

    result = client.post(
        f"/projects/{test_project.id}/invite?user={invited_user.email}",
        headers={"MyAuthorization": f"Bearer {test_token}"},
    )

    assert result.status_code == 201


def test_invite_to_project_unauthorized(
    client: TestClient,
    test_user: dto.User,
    test_projects: list[project_dto.Project],
    participant_token: str,
    invited_user: dto.User,
) -> None:
    test_project = test_projects[0]

    result = client.post(
        f"/projects/{test_project.id}/invite?user={invited_user.email}",
        headers={"MyAuthorization": f"Bearer {participant_token}"},
    )

    assert result.status_code == 403
