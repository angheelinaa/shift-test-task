from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from shift_test_task.user.models import Role


class UserRead(BaseModel):
    username: str
    full_name: str
    salary: int | None
    promotion_date: date | None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserRead):
    password: str


class User(UserRead):
    id: int
    role: Role | str
    is_active: bool


class UpdateSalary(BaseModel):
    salary: Optional[int | None] = None
    promotion_date: Optional[date | None] = None
