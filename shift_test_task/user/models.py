from datetime import date
import enum

from sqlalchemy.orm import Mapped, mapped_column

from shift_test_task.core.database import Base


class Role(str, enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str]
    hashed_password: Mapped[str]
    salary: Mapped[int] = mapped_column(nullable=True)
    promotion_date: Mapped[date] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(default=Role.user)
    is_active: Mapped[bool] = mapped_column(default=True)

    @property
    def is_admin(self):
        return self.role == Role.admin
