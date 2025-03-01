from sqlalchemy import Delete, Insert, Select, Update, delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.permissions.enums import UserRole
from src.permissions.models import Permission
from src.users.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_user_id(self, user_id: int) -> User | None:
        """Get one user by its id"""
        query: Select = select(User).where(User.id == user_id)

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_user_by_user_email(self, email: str) -> User | None:
        """Get one user by its email"""
        query: Select = select(User).where(User.email == email)

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def update_user(self, user_id: int, email: str, password: str) -> User | None:
        """Updates a user by ID and returns True if updated, False if not found."""
        query: Update = update(User).where(User.id == user_id).values(email=email, password=password).returning(User)

        try:
            result = self.session.execute(query)
            self.session.commit()
            return result.scalar_one_or_none()
        except IntegrityError:
            self.session.rollback()
            return None

    def create_user(self, email: str, password: str) -> User | None:
        """Inserts a new user and returns the created User object."""
        query: Insert = insert(User).values(email=email, password=password).returning(User)

        try:
            result = self.session.execute(query)
            self.session.commit()
            return result.scalar_one_or_none()
        except IntegrityError:
            self.session.rollback()
            return None

    def delete_user(self, user_id: int) -> bool:
        """Deletes a user by ID and returns True if deleted, False otherwise."""
        query: Delete = delete(User).where(User.id == user_id)

        result = self.session.execute(query)

        if result.rowcount() > 0:
            self.session.commit()
            return True
        return False

    def is_owner(self, owner_id: int, project_id: int) -> bool:
        query: Select = select(Permission).where(
            Permission.project_id == project_id, Permission.user_id == owner_id, Permission.user_role == UserRole.OWNER
        )

        result = self.session.execute(query)
        return result.scalar() is not None
