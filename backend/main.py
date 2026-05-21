from contextlib import asynccontextmanager
import uvicorn
from app.users.views import router as user_router
from app.api_v1 import router as router_v1
from fastapi import FastAPI
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
