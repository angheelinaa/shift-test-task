from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from shift_test_task.auth.security import get_current_active_user
from shift_test_task.core.database import get_db
from shift_test_task.user.schemas import (
    UserCreate,
    User as UserSchemas,
    UpdateSalary
)
from shift_test_task.user.crud import (
    _create_user,
    _get_user_by_username,
    _get_users,
    _get_user,
    _disable_user,
    _update_user_salary_info
)
from shift_test_task.core.role_permission_decorator import check_admin_role
from shift_test_task.user.models import User as UserOrm, Role


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
@check_admin_role
def create_user(
        user: UserCreate = Depends(),
        current_user: UserOrm = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    db_user = _get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username already registered"
        )
    return _create_user(db=db, user=user)


@router.get("/", response_model=list[UserSchemas])
@check_admin_role
def read_users(
        current_user: UserOrm = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    db_users = _get_users(db=db)
    users = [UserSchemas.model_validate(db_user) for db_user in db_users]
    return users


@router.patch("/disable/{username}", response_model=UserSchemas)
@check_admin_role
def disable_user(
        username: str,
        current_user: UserOrm = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    db_user = _get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if db_user.role == Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden disable the admin"
        )
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already disabled"
        )
    user = UserSchemas.model_validate(_disable_user(db=db, user=db_user))
    return user


@router.patch("/salary/{username}")
@check_admin_role
def update_user_salary_info(
        username: str,
        request: UpdateSalary = Depends(),
        current_user: UserOrm = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    db_user = _get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if db_user.role == Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden change the admin`s salary"
        )
    user = UserSchemas.model_validate(
        _update_user_salary_info(
            db=db, user=db_user, update_params=request
        )
    )
    return user


@router.get("/{user_id}", response_model=UserSchemas)
@check_admin_role
def read_user(
        user_id: int,
        current_user: UserOrm = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    db_user = _get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = UserSchemas.model_validate(db_user)
    return user
