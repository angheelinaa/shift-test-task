from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from shift_test_task.auth.token_schemas import Token
from shift_test_task.auth.security import (
    create_access_token,
    get_current_active_user,
    authenticate_user)
from shift_test_task.core.database import get_db
from shift_test_task.user.models import User
from shift_test_task.user.schemas import UserRead

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    payload = {"sub": user.username}
    access_token = create_access_token(payload)
    return Token(access_token=access_token, token_type="Bearer")


@router.get("/salary_info", response_model=UserRead)
def get_current_user_salary_info(
        current_user: User = Depends(get_current_active_user)
):
    user = UserRead.model_validate(current_user)
    return user
