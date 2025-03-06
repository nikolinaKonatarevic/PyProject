from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.sync_engine import get_db_session
from src.exceptions import DeleteFailedException, NotFoundException, PostFailedException, UpdateFailedException
from src.users import dto
from src.users.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_by_id(self, user_id: int) -> dto.User:
        user = self.repository.get_user_by_user_id(user_id)
        if not user:
            raise NotFoundException()
        return dto.User.model_validate(user)

    def create_user(self, user_data: dto.UserCreate) -> dto.User:
        user = self.repository.create_user(str(user_data.email), user_data.password)
        if user:
            return dto.User.model_validate(user)
        raise PostFailedException()

    def update_user(self, user_data: dto.UserUpdate) -> dto.User:
        user = self.repository.update_user(user_data.id, str(user_data.email), user_data.password)
        if user:
            return dto.User.model_validate(user)
        raise UpdateFailedException()

    def delete_user(self, user_id: int) -> bool:
        user = self.repository.get_user_by_user_id(user_id)
        if user is None:
            raise DeleteFailedException()
        return self.repository.delete_user(user_id)


def get_user_service(db: Session = Depends(get_db_session)):
    repository = UserRepository(db)
    return UserService(repository)
