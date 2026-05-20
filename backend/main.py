from contextlib import asynccontextmanager
from typing import Annotated
from core.models import Base, db_helper
import uvicorn
from app.users.views import router as user_router
from fastapi import Body
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import EmailStr


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
