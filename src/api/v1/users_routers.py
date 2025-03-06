from fastapi import APIRouter, Depends
from starlette import status

from src.deps import get_user_service
from src.users import dto
from src.users.services import UserService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/{user_id}",
    response_model=dto.User,
    status_code=status.HTTP_200_OK,
    description="Returns user with the certain ID",
)
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> dto.User:
    """
    Get a user by ID.
    """
    return user_service.get_user_by_id(user_id)


@user_router.post("/", response_model=dto.User, status_code=status.HTTP_201_CREATED, description="Creates a new user")
def create_user(user_data: dto.UserCreate, user_service: UserService = Depends(get_user_service)) -> dto.User:
    """
    Create a new user.
    """
    return user_service.create_user(user_data)


@user_router.patch(
    "/{user_id}", response_model=dto.UserUpdate, status_code=status.HTTP_200_OK, description="Updates user"
)
def update_user(user_data: dto.UserUpdate, user_service: UserService = Depends(get_user_service)) -> dto.User:
    """
    Update a user by ID.
    """
    return user_service.update_user(user_data)


@user_router.delete("/{user_id}")
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> bool:
    """
    Delete a user by ID.
    """
    return user_service.delete_user(user_id)
