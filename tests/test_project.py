from starlette import status
from starlette.testclient import TestClient

from src.api.users.models import User


# GET
def test_get_projects(
    client: TestClient,
    create_test_user: User,
    create_test_projects,
    create_test_token: str,
) -> None:
    result = client.get("/v1/projects", headers={"MyAuthorization": f"Bearer {create_test_token}"})
    assert result.status_code == status.HTTP_200_OK


def test_get_project(
    client: TestClient,
    create_test_user: User,
    create_test_projects,
    create_test_token: str,
) -> None:
    test_project = create_test_projects[0]

    result = client.get(f"/v1/projects/{test_project.id}/info",
                        headers={"MyAuthorization": f"Bearer {create_test_token}"})

    assert result.json() == {
        "id": str(test_project.id),
        "name": test_project.name,
        "description": test_project.description,
        "owner_id": str(test_project.owner_id),
    }


def test_get_project_unauthorized(
    client: TestClient,
    create_test_user: User,
    create_test_projects,
    create_unauthorized_token: str,
) -> None:
    test_project = create_test_projects[0]

    res = client.get(
        f"/v1/projects/{test_project.id}/info",
        headers={"MyAuthorization": f"Bearer {create_unauthorized_token}"},
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_get_project_nonexisting(
    client: TestClient,
    create_test_user: User,
    create_test_token: str,
) -> None:
    res = client.get(
        "/v1/projects/340002221111/info",
        headers={"MyAuthorization": f"Bearer {create_test_token}"},
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


# CREATE
def test_create_project(
    client: TestClient,
    create_test_user: User,
    create_test_token: str,
) -> None:
    data = {"name": "project test", "description": "Description for the test project"}

    result = client.post("/v1/projects/", json=data, headers={"MyAuthorization": f"Bearer {create_test_token}"})

    assert (
        result.json()["name"] == data["name"]
        and result.json()["owner_id"] == str(create_test_user.id)
        and result.json()["description"] == data["description"]
    )


# UPDATE
def test_update_project(
    client: TestClient,
    create_test_user: User,
    create_test_projects,
    create_test_token: str,
) -> None:
    test_project = create_test_projects[0]
    data = {"name": "updated_project", "description": "Updated description"}

    result = client.put(
        f"/v1/projects/{test_project.id}/info",
        json=data,
        headers={"MyAuthorization": f"Bearer {create_test_token}"},
    )

    assert result.json()["name"] == data["name"] and result.json()["description"] == data["description"]


def test_update_project_nonexisting(
    client: TestClient,
    create_test_user: User,
    create_test_token: str,
) -> None:
    data = {"name": "updated_project", "description": "Updated description"}

    result = client.put(
        "/projects/340002221111/info",
        json=data,
        headers={"MyAuthorization": f"Bearer {create_test_token}"},
    )

    assert result.status_code == status.HTTP_403_FORBIDDEN

# DELETE
def test_delete_project(
    client: TestClient,
    create_test_user: User,
    create_test_projects,
    create_test_token: str,
) -> None:
    test_project = create_test_projects[0]

    result = client.delete(f"/v1/projects/{test_project.id}",
                           headers={"MyAuthorization": f"Bearer {create_test_token}"})

    assert result.status_code == status.HTTP_204_NO_CONTENT


def test_delete_project_nonexisting(
    client: TestClient,
    create_test_user: User,
    create_test_token: str,
) -> None:
    result = client.delete(
        "/projects/340002221111/",
        headers={"MyAuthorization": f"Bearer {create_test_token}"},
    )

    assert result.status_code == status.HTTP_404_NOT_FOUND

def test_delete_project_participant(
    client: TestClient,
    create_test_user: User,
        create_test_projects,
    create_participant_token: str,
) -> None:
    test_project = create_test_projects[0]

    result = client.delete(
        f"/v1/projects/{test_project.id}",
        headers={"MyAuthorization": f"Bearer {create_participant_token}"},
    )

    assert result.status_code == status.HTTP_403_FORBIDDEN


# INVITE
def test_invite_to_project(
    client: TestClient,
    create_test_user: User,
        create_test_projects,
    create_test_token: str,
        create_invited_user: User,
) -> None:
    test_project = create_test_projects[0]

    result = client.post(
        f"/projects/{test_project.id}/invite?user={create_invited_user.email}",
        headers={"MyAuthorization": f"Bearer {create_test_token}"},
    )

    assert result.status_code == status.HTTP_201_CREATED


def test_invite_to_project_unauthorized(
    client: TestClient,
    create_test_user: User,
    create_test_projects,
    create_participant_token: str,
        create_invited_user: User,
) -> None:
    test_project = create_test_projects[0]

    result = client.post(
        f"/projects/{test_project.id}/invite?user={create_invited_user.email}",
        headers={"MyAuthorization": f"Bearer {create_participant_token}"},
    )

    assert result.status_code == status.HTTP_403_FORBIDDEN
