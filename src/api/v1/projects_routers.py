from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.deps import get_project_service
from src.projects import project_dto
from src.projects.services import ProjectService
from src.users import dto
from src.users.user_deps import get_curr_user

project_router = APIRouter(prefix="/projects", tags=["projects"])


@project_router.get("/", status_code=status.HTTP_200_OK)
def get_projects(
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    project_service: ProjectService = Depends(get_project_service),
) -> list[project_dto.Project]:
    return project_service.get_all_projects(curr_user)


@project_router.get("/{project_id}/info", status_code=status.HTTP_200_OK)
def get_project_info(
    project_id: int,
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    project_service: ProjectService = Depends(get_project_service),
) -> project_dto.Project:
    return project_service.get_project_info(curr_user, project_id)


@project_router.post("/", response_model=project_dto.Project, status_code=status.HTTP_201_CREATED)
def create_project(
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    project_data: project_dto.ProjectCreate,
    project_service: ProjectService = Depends(get_project_service),
) -> project_dto.Project:
    return project_service.create_project(project_data, curr_user)


@project_router.patch("/{project_id}/info", status_code=status.HTTP_200_OK)
def update_project(
    project_id: int,
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    project_data: project_dto.ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service),
) -> project_dto.Project:
    return project_service.update_project(project_id, curr_user, project_data)


@project_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    project_id: int,
    project_service: ProjectService = Depends(get_project_service),
) -> None:
    project_service.delete_project(project_id, curr_user)
    return None


@project_router.post("/{project_id}/invite")
def invite(
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    user_id: int,
    project_id: int,
    project_service: ProjectService = Depends(get_project_service),
) -> bool:
    return project_service.invite(project_id, user_id, curr_user)
