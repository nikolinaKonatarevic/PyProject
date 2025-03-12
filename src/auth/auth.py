from datetime import datetime, timedelta, timezone

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import AuthenticationError


class MyOAuthPasswordBearer(OAuth2PasswordBearer):
    """class for handling Bearer token authentication"""

    def __call__(self, request: Request) -> str | None:
        auth = request.headers.get("Authorization")
        scheme, token = get_auth_scheme_token(auth)
        if not auth or scheme.lower() != "bearer":
            raise AuthenticationError()
        return token


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = MyOAuthPasswordBearer(tokenUrl="/v1/users/login")


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_auth_scheme_token(auth_header_value: str | None) -> tuple[str, str]:
    if not auth_header_value:
        return "", ""
    scheme, _, token = auth_header_value.partition(" ")
    return scheme, token


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
