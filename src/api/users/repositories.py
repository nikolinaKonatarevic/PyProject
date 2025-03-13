from sqlalchemy import Delete, Insert, Select, Update, delete, insert, select, update
from sqlalchemy.orm import Session

from src.api.auth.auth import verify_password
from src.api.permissions.enums import UserRole
from src.api.permissions.models import Permission
from src.api.users.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_user_id(self, user_id: int) -> User | None:
        """Get one user by its id"""
        query: Select = select(User).where(User.id == user_id)

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_user_by_email(self, email: str) -> User | None:
        """Get one user by its email"""
        query: Select = select(User).where(User.email == email)

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def update_user(self, user_id: int, email: str, password_hash: str) -> User | None:
        """Updates a user by ID and returns True if updated, False if not found."""
        query: Update = (
            update(User).where(User.id == user_id).values(email=email, password_hash=password_hash).returning(User)
        )

        result = self.session.execute(query)
        if result:
            self.session.commit()
        return result.scalar_one_or_none()

    def create_user(self, email: str, password_hash: str) -> User | None:
        """Inserts a new user and returns the created User object."""

        query: Insert = insert(User).values(email=email, password_hash=password_hash).returning(User)

        result = self.session.execute(query)

        self.session.commit()
        return result.scalar_one_or_none()

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

    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
