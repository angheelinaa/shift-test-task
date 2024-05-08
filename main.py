from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from shift_test_task.core.create_admin import create_admin
from shift_test_task.core.database import engine, Base
from shift_test_task.user.views import router as user_router
from shift_test_task.auth.views import router as auth_router


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    await create_admin()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app)
