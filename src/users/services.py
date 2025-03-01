from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.data_base.sync_engine import get_db_session
from src.users import dto
from src.users.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_by_id(self, user_id: int) -> dto.User:
        user = self.repository.get_user_by_user_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist")
        return dto.User.model_validate(user)

    def create_user(self, user_data: dto.UserCreate) -> dto.User:
        user = self.repository.create_user(str(user_data.email), user_data.password)
        if user:
            return dto.User.model_validate(user)
        raise HTTPException(status_code=404, detail="Creating user did not succeed")

    def update_user(self, user_data: dto.UserUpdate) -> dto.User:
        user = self.repository.update_user(user_data.id, str(user_data.email), user_data.password)
        if user:
            return dto.User.model_validate(user)
        raise HTTPException(status_code=404, detail="Updating user did not succeed")

    def delete_user(self, user_id: int) -> bool:
        user = self.repository.get_user_by_user_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist")
        return self.repository.delete_user(user_id)


def get_user_service(db: Session = Depends(get_db_session)):
    repository = UserRepository(db)
    return UserService(repository)
