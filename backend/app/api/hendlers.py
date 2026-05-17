from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import ShowUser, UserCreate

from core.session import get_db

user_router = APIRouter()

async def _create_new_user(body: UserCreate, core) -> ShowUser:
    async with core as session:
        async with session.begin():
            user_dal =UserDAL(session)
            user = await user_dal.create_user(
                username=body.username,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
                user_id=user.user_id,
                username=user.username,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )

@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, core: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, core)
