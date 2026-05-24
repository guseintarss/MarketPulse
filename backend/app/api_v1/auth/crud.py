from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.auth import utils as auth_utils


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
    password: str,
    is_active: bool = True,
) -> User:
    hashed_password = auth_utils.hash_password(password)
    user = User(
        username=username,
        email=email,
        password=hashed_password,
        is_active=is_active,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_username(
    session: AsyncSession,
    username: str,
) -> User | None:
    stmt = select(User).where(User.username == username)
    return await session.scalar(stmt)


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)
