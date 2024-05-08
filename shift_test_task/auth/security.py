from datetime import timedelta, datetime

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from shift_test_task.auth.token_schemas import TokenData
from shift_test_task.core.config import settings
from shift_test_task.core.database import get_db
from shift_test_task.user.crud import _get_user_by_username
from shift_test_task.auth.hashing import Hasher
from shift_test_task.user.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(db: Session, username: str, password: str):
    db_user = _get_user_by_username(db=db, username=username)
    if not db_user:
        return False
    if not Hasher.verify_password(password, db_user.hashed_password):
        return False
    return db_user


def create_access_token(
        payload: dict,
        key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM,
        expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expires_delta: timedelta | None = None
):
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm)
    return encoded_jwt


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    db_user = _get_user_by_username(
        db=db, username=token_data.username
    )
    if db_user is None:
        raise credentials_exception
    return db_user


def get_current_active_user(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
