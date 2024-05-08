from sqlalchemy.orm import Session

from . import models, schemas
from shift_test_task.auth.hashing import Hasher


def _get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def _get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def _get_users(db: Session):
    return db.query(models.User).all()


def _create_user(db: Session, user: schemas.UserCreate):
    hashed_password = Hasher.get_hashed_password(user.password)
    db_user = models.User(
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        salary=user.salary,
        promotion_date=user.promotion_date
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def _disable_user(db: Session, user: models.User):
    user.is_active = False
    db.commit()
    return user


def _update_user_salary_info(
        db: Session,
        user: models.User,
        update_params: schemas.UpdateSalary
):
    if update_params.salary:
        user.salary = update_params.salary
    if update_params.promotion_date:
        user.promotion_date = update_params.promotion_date
    db.commit()
    return user
