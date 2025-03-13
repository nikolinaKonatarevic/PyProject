from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.auth import token
from src.api.deps import get_user_service
from src.api.users import dto
from src.api.users.services import UserService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/auth", response_model=dto.User, status_code=status.HTTP_201_CREATED, description="Creates a new user"
)
def create_user(user_data: dto.UserCreate, user_service: UserService = Depends(get_user_service)) -> dto.User:
    """
    Create a new user.
    """
    return user_service.create_user(user_data)


@user_router.post("/login", response_model=token.Token, status_code=status.HTTP_200_OK)
def login(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: UserService = Depends(get_user_service)
) -> token.Token:
    """
    Delete a user by ID.
    """
    return user_service.login(login_data)
