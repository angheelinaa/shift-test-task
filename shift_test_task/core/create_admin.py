from sqlalchemy.orm import Session

from shift_test_task.auth.hashing import Hasher
from shift_test_task.core.database import SessionLocal
from shift_test_task.user.models import User, Role


async def create_admin():
    db: Session = SessionLocal()

    hashed_password = Hasher.get_hashed_password("admin")
    db_admin = User(
        username="admin",
        full_name="admin",
        hashed_password=hashed_password,
        role=Role.admin
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
