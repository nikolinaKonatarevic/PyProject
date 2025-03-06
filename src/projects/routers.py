from typing import List

from fastapi import APIRouter, Depends, status

from src.projects import dto
from src.projects.services import ProjectService, get_project_service

project_router = APIRouter(prefix="/projects", tags=["projects"])


@project_router.get("/", status_code=status.HTTP_200_OK)
def get_projects(user_id: int, project_service: ProjectService = Depends(get_project_service)) -> List[dto.Project]:
    return project_service.get_all_projects(user_id)


@project_router.get("/{project_id}/info", status_code=status.HTTP_200_OK)
def get_project_info(
    project_id: int, user_id: int, project_service: ProjectService = Depends(get_project_service)
) -> dto.Project:
    return project_service.get_project_info(user_id, project_id)


@project_router.put("/{project_id}/info", response_model=dto.Project, status_code=status.HTTP_201_CREATED)
def create_project(
    user_id: int, project_data: dto.ProjectCreate, project_service: ProjectService = Depends(get_project_service)
) -> dto.Project:
    return project_service.create_project(project_data, user_id)


@project_router.patch("/{project_id}/info", status_code=status.HTTP_200_OK)
def update_project(
    project_id: int,
    user_id: int,
    project_data: dto.ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service),
) -> dto.Project:
    return project_service.update_project(project_id, user_id, project_data)


@project_router.delete("/{project_id}")
def delete_project(
    user_id: int, project_id: int, project_service: ProjectService = Depends(get_project_service)
) -> bool:
    return project_service.delete_project(project_id, user_id)
