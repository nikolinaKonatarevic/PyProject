from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm

from src.api.auth import token
from src.api.auth.auth import create_access_token, get_password_hash
from src.api.config import settings
from src.api.exceptions import (
    AuthenticationError,
    DeleteFailedException,
    InvalidInputException,
    NotFoundException,
    PostFailedException,
    UpdateFailedException,
)
from src.api.users import dto
from src.api.users.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_by_id(self, user_id: int) -> dto.User:
        user = self.repository.get_user_by_user_id(user_id)
        if not user:
            raise NotFoundException()
        return dto.User.model_validate(user)

    def update_user(self, user_data: dto.UserUpdate) -> dto.User:
        user = self.repository.update_user(user_data.id, str(user_data.email), user_data.password_hash)
        if user:
            return dto.User.model_validate(user)
        raise UpdateFailedException()

    def delete_user(self, user_id: int) -> bool:
        user = self.repository.get_user_by_user_id(user_id)
        if user is None:
            raise DeleteFailedException()
        return self.repository.delete_user(user_id)

    def create_user(self, user_data: dto.UserCreate) -> dto.User:
        if not user_data.password == user_data.repeat_password:
            raise InvalidInputException(message="Passwords are not matching")
        password_hash = get_password_hash(user_data.password)
        user = self.repository.create_user(str(user_data.email), password_hash)
        if user:
            return dto.User.model_validate(user)
        raise PostFailedException(message="Creating user failed")

    def login(self, login_data: OAuth2PasswordRequestForm) -> token.Token:
        user = self.repository.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise AuthenticationError()

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        return token.Token(access_token=access_token, token_type="bearer")
