from sqlalchemy import Delete, Insert, Select, Update, delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.exceptions import PostFailedException
from src.api.permissions.enums import RequestStatus, UserRole
from src.api.permissions.models import Permission
from src.api.projects.models import Project


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_project_by_project_id(self, project_id: int) -> Project | None:
        """Get one project by its id"""
        query: Select = select(Project).where(Project.id == project_id)

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_project_by_name(self, name: str) -> Project | None:
        """Get one project with a certain name"""
        query: Select = select(Project).where(Project.name == name)

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_all_projects(self) -> list[Project] | None:
        """Executing query for getting all projects"""
        query: Select = select(Project)

        result = self.session.execute(query)
        projects = list(result.scalars().all())
        return projects if projects else None

    def create_project(self, name: str, description: str, owner_id: int) -> Project | None:
        """Creates a new project and returns the created Project object"""
        query: Insert = insert(Project).values(name=name, description=description, owner_id=owner_id).returning(Project)
        try:
            result = self.session.execute(query)
            project = result.scalar_one_or_none()

            if project:
                self.give_permission(project.id, owner_id, UserRole.OWNER)
                self.session.commit()
                return project

        except IntegrityError:
            self.session.rollback()
            raise PostFailedException(message="Failed to Post the Project to db")
        return None

    def update_project(self, project_id: int, name: str, description: str) -> Project | None:
        """Updates a project by ID and returns True if updated, False if not found."""
        query: Update = (
            update(Project).where(Project.id == project_id).values(name=name, description=description)
        ).returning(Project)

        result = self.session.execute(query)
        self.session.commit()
        return result.scalar_one_or_none()

    def delete_project(self, project_id: int) -> bool:
        """Deletes a project by ID and returns True if deleted, False otherwise."""
        query: Delete = delete(Project).where(Project.id == project_id)

        result = self.session.execute(query)

        if result:
            self.session.commit()
            return True
        self.session.rollback()
        return False

    def has_permission(
        self, project_id: int, curr_user_id: int, roles: tuple[UserRole, ...] = (UserRole.OWNER, UserRole.PARTICIPANT)
    ) -> bool:
        query: Select = (
            select(Permission)
            .where(Permission.project_id == project_id, Permission.user_id == curr_user_id)
            .where(Permission.user_role.in_(roles))
        )

        result = self.session.execute(query)
        return result.scalar() is not None

    def get_projects_for_user(
        self, user_id: int, roles: tuple[UserRole, ...] = (UserRole.OWNER, UserRole.PARTICIPANT)
    ) -> list[Project]:
        """
        Returns a list of projects where user has a certain role.
        """
        query: Select = (
            select(Project)
            .join(Permission, Project.id == Permission.project_id)
            .where(Permission.user_id == user_id)
            .where(Permission.user_role.in_(roles))
        )

        result = self.session.execute(query)
        projects = list(result.scalars().all())
        return projects

    def give_permission(
        self, project_id: int, user_id: int, user_role: UserRole = UserRole.PARTICIPANT
    ) -> Permission | None:
        """
        Gives permission for the user on a specific project.
        """
        request_status = RequestStatus.ACCEPTED

        query: Insert = (
            insert(Permission)
            .values(user_id=user_id, project_id=project_id, user_role=user_role, request_status=request_status)
            .returning(Permission)
        )

        try:
            result = self.session.execute(query)
            self.session.commit()
            return result.scalar_one_or_none()
        except IntegrityError:
            self.session.rollback()

        return None
