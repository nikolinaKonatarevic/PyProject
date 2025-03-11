from src.exceptions import (
    AccessDeniedException,
    DeleteFailedException,
    NotFoundException,
    PostFailedException,
    UpdateFailedException,
)
from src.permissions.enums import UserRole
from src.projects import project_dto
from src.projects.repositories import ProjectRepository
from src.users import dto


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def get_all_projects(self, curr_user: dto.User) -> list[project_dto.Project]:
        result = self.repository.get_projects_for_user(curr_user.id)
        if not result:
            raise NotFoundException()
        return [project_dto.Project.model_validate(project) for project in result]

    def get_project_info(self, curr_user: dto.User, project_id: int) -> project_dto.Project:
        if not self.repository.has_permission(project_id, curr_user.id):
            raise AccessDeniedException()

        result = self.repository.get_project_by_project_id(project_id)
        if not result:
            raise NotFoundException()

        return project_dto.Project.model_validate(result)

    def create_project(self, project_data: project_dto.ProjectCreate, curr_user: dto.User) -> project_dto.Project:
        project = self.repository.create_project(project_data.name, project_data.description, curr_user.id)
        if not project:
            raise PostFailedException()
        return project_dto.Project.model_validate(project)

    def update_project(
        self, project_id: int, curr_user: dto.User, project_data: project_dto.ProjectUpdate
    ) -> project_dto.Project:
        if not self.repository.has_permission(project_id, curr_user.id):
            raise AccessDeniedException()

        if not self.repository.get_project_by_project_id(project_id):
            raise NotFoundException()
        result = self.repository.update_project(project_id, **project_data.model_dump())
        if result is None:
            raise UpdateFailedException()
        return project_dto.Project.model_validate(result)

    def delete_project(self, project_id: int, curr_user: dto.User) -> bool:
        if not self.repository.has_permission(project_id, curr_user.id, (UserRole.OWNER,)):
            raise AccessDeniedException()

        if not self.repository.get_project_by_project_id(project_id):
            raise NotFoundException()

        result = self.repository.delete_project(project_id)

        if not result:
            raise DeleteFailedException()
        return result

    def invite(self, project_id: int, user_id: int, curr_user: dto.User) -> bool:
        if not self.repository.has_permission(curr_user.id, project_id, (UserRole.OWNER,)):
            raise AccessDeniedException()

        perm = self.repository.give_permission(project_id, user_id)
        if not perm:
            return False
        return True
