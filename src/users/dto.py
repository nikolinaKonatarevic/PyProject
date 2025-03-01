from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    id: int
    password: str


class User(UserBase):
    id: int
    password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UsersPaginated(BaseModel):
    page: int
    per_page: int
    total_users: int
    total_pages: int
    # users: List[User]
