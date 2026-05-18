from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Union
from .core.dals import UserDAL
from .models import ShowUser, UserCreate, DeleteUserResponse, UpdateUserResponse

from logging import getLogger

from core.session import get_db

logger = getLogger(__name__)

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

async def _delete_user(user_id, core) -> Union[UUID, None]:
    async with core as session:
        async with session.begin():
            user_dal = UserDAL(session)
            delete_user_id = await user_dal.delete_user(
                user_id=user_id,
            )
            return delete_user_id


async def _update_user(body, core) -> Union[UUID, None]:
    async with core as session:
        async with session.begin():
            user_dal = UserDAL(session)
            update_user_id = await user_dal.user_update(
                **body.dict()
            )
            return update_user_id

async def _get_user_by_id(user_id, core) -> Union[ShowUser, None]:
    async with core as session:
        async with session.begin():
            user_dal = UserDAL()
            user = await user_dal.get_user_by_id(
                user_id=user_id
            )
            if user is not None:
                return ShowUser(
                    user_id=user.user_id,
                    username=user.username,
                    surname=user.surname,
                    email=user.email,
                    is_active=user.is_active,
                )

@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, core: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, core)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") 

@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, core:AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    delete_user_id = await _delete_user(user_id, core)
    if delete_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(delete_user_id=delete_user_id)

@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, core: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, core)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user

@user_router.patch("/", response_model=UpdateUserResponse)
async def update_user_by_id(
    user_id: UUID, body: UpdateUserResponse, core: AsyncSession = Depends(get_db)
) -> UpdateUserResponse:
    update_user_params = body.dict(exclude_none=True)
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user = await _get_user_by_id(user_id, core)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    try:
        update_user_by_id = await _update_user(update_user_params=update_user_params, core=core, user_id=user_id)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

    return UpdateUserResponse(update_user_id=update_user_id)