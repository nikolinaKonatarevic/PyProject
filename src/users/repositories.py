from typing import Sequence

from sqlalchemy import Delete, Insert, Row, Select, Update, delete, insert, select, update
from sqlalchemy.orm import Session

from src.users.dto import UserCreateDTO, UserUpdateDTO
from src.users.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_user_id(self, id: int):
        """Get one user by its id"""
        query: Select = select(User).where(User.id == id)

        result = self.session.execute(query)
        return result

    def get_user_by_user_email(self, email: str):
        """Get one user by its email"""
        query: Select = select(User).where(User.email == email)

        result = self.session.execute(query)
        return result

    def get_all_users(self):
        """Executing query for getting all users"""
        query: Select = select(User)

        result = self.session.execute(query)

        rows: Sequence[Row] = result.fetchall()
        return rows

    def update_user(self, user_id: int, user_data: UserUpdateDTO) -> bool:
        """Updates a user by ID and returns True if updated, False if not found."""
        query: Update = update(User).where(User.id == user_id).values(**user_data.model_dump())

        result = self.session.execute(query)
        self.session.commit()

        return result.rowcount() > 0

    def insert_user(self, user_data: UserCreateDTO) -> User | None:
        """Inserts a new user and returns the created User object."""
        query: Insert = insert(User).values(**user_data.model_dump()).returning(User)

        result = self.session.execute(query)
        self.session.commit()

        return result.scalar_one_or_none()

    def delete_user(self, user_id: int) -> bool:
        """Deletes a user by ID and returns True if deleted, False otherwise."""
        query: Delete = delete(User).where(User.id == user_id)

        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0
