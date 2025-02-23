from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class UserBaseDTO(BaseModel):
    email: EmailStr


class UserCreateDTO(UserBaseDTO):
    password: str


class UserUpdateDTO(UserBaseDTO):
    password: str


class UserResponseDTO(UserCreateDTO):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UsersPaginated(BaseModel):
    page: int
    per_page: int
    total_users: int
    total_pages: int
    users: List[UserResponseDTO]
