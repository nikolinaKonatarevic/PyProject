from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.data_base.sync_engine import get_db_session
from src.permissions.enums import UserRole
from src.projects import dto
from src.projects.repositories import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def get_all_projects(self, user_id: int) -> List[dto.Project]:
        result = self.repository.get_projects_for_user(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User has not projects")
        return [dto.Project.model_validate(project) for project in result]

    def get_project_info(self, user_id: int, project_id: int) -> dto.Project:
        if not self.repository.get_project_by_project_id(project_id):
            raise HTTPException(status_code=404, detail=f"Project with id {project_id} is not found")

        if not self.repository.has_permission(project_id, user_id):
            raise HTTPException(
                status_code=403, detail=f"User with id {user_id} not authorized to access project with id {project_id}"
            )

        result = self.repository.get_project_by_project_id(project_id)
        if not result:
            raise HTTPException(status_code=500)
        return dto.Project.model_validate(result)

    def create_project(self, project_data: dto.ProjectCreate, owner_id: int) -> dto.Project:
        project = self.repository.create_project(project_data.name, project_data.description, owner_id)
        if not project:
            raise HTTPException(status_code=404, detail="Creating project did not succeed")
        return dto.Project.model_validate(project)

    def update_project(self, project_id: int, user_id: int, project_data: dto.ProjectUpdate) -> dto.Project:
        if not self.repository.get_project_by_project_id(project_id):
            raise HTTPException(status_code=404, detail=f"Project with id {project_id} is not found")

        if not self.repository.has_permission(project_id, user_id):
            raise HTTPException(
                status_code=403, detail=f"User with id {user_id} not authorized to access project with id {project_id}"
            )

        result = self.repository.update_project(project_id, *project_data)
        if result is None:
            raise HTTPException(status_code=404, detail="Updating project did not succeed")
        return dto.Project.model_validate(result)

    def delete_project(self, project_id: int, user_id: int) -> bool:
        if not self.repository.get_project_by_project_id(project_id):
            raise HTTPException(status_code=404, detail=f"Project with id {project_id} is not found")

        if not self.repository.has_permission(project_id, user_id):
            raise HTTPException(
                status_code=403, detail=f"User with id {user_id} not authorized to access project with id {project_id}"
            )

        result = self.repository.delete_project(project_id)
        return result

    def invite(self, project_id: int, user_id: int, owner_id: int) -> bool:
        if not self.repository.has_permission(owner_id, project_id, (UserRole.OWNER,)):
            raise HTTPException(status_code=403, detail="Only project owner can invite to project")

        perm = self.repository.give_permission(project_id, user_id)
        if not perm:
            return False
        return True


def get_project_service(db: Session = Depends(get_db_session)):
    repository = ProjectRepository(db)
    return ProjectService(repository)
