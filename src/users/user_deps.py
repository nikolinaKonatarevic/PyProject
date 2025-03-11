from typing import Annotated

from fastapi.params import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.auth.auth import MyOAuthPasswordBearer
from src.config import settings
from src.database.sync_engine import get_db_session
from src.exceptions import AccessDeniedException
from src.users import dto
from src.users.models import User

oauth2_scheme = MyOAuthPasswordBearer(tokenUrl="/v1/users/login")


def get_curr_user(
    db: Annotated[Session, Depends(get_db_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dto.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise AccessDeniedException(message="Access denied")

    except JWTError:
        raise AccessDeniedException(message="Access denied. JWTError")
    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise AccessDeniedException(message="Access denied. Wrong credentials")
    return dto.User.model_validate(user)
