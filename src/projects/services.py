from src.exceptions import (
    AccessDeniedException,
    DeleteFailedException,
    NotFoundException,
    PostFailedException,
    UpdateFailedException,
)
from src.permissions.enums import UserRole
from src.projects import dto
from src.projects.repositories import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def get_all_projects(self, user_id: int) -> list[dto.Project]:
        result = self.repository.get_projects_for_user(user_id)
        if not result:
            raise NotFoundException()
        return [dto.Project.model_validate(project) for project in result]

    def get_project_info(self, user_id: int, project_id: int) -> dto.Project:
        result = self.repository.get_project_by_project_id(project_id)
        if not result:
            raise NotFoundException()
        if not self.repository.has_permission(project_id, user_id):
            raise AccessDeniedException()

        return dto.Project.model_validate(result)

    def create_project(self, project_data: dto.ProjectCreate, owner_id: int) -> dto.Project:
        project = self.repository.create_project(project_data.name, project_data.description, owner_id)
        if not project:
            raise PostFailedException()
        return dto.Project.model_validate(project)

    def update_project(self, project_id: int, user_id: int, project_data: dto.ProjectUpdate) -> dto.Project:
        if not self.repository.get_project_by_project_id(project_id):
            raise NotFoundException()

        if not self.repository.has_permission(project_id, user_id):
            raise AccessDeniedException()

        result = self.repository.update_project(project_id, *project_data)
        if result is None:
            raise UpdateFailedException()
        return dto.Project.model_validate(result)

    def delete_project(self, project_id: int, user_id: int) -> bool:
        if not self.repository.get_project_by_project_id(project_id):
            raise NotFoundException()

        if not self.repository.has_permission(project_id, user_id):
            raise AccessDeniedException()

        result = self.repository.delete_project(project_id)
        if not result:
            raise DeleteFailedException()
        return result

    def invite(self, project_id: int, user_id: int, owner_id: int) -> bool:
        if not self.repository.has_permission(owner_id, project_id, (UserRole.OWNER,)):
            raise AccessDeniedException()

        perm = self.repository.give_permission(project_id, user_id)
        if not perm:
            return False
        return True
