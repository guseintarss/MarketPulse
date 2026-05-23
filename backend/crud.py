import asyncio

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    # print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    firstname: str | None = None,
    lastname: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        firstname=firstname,
        lastname=lastname,
    )
    session.add(profile)
    await session.commit()
    return profile


async def main():
    async with db_helper.session_factory() as session:
        # await  create_user(session=session, username="jhon")
        # await  create_user(session=session, username="Bob")
        user_bob = await get_user_by_username(session=session, username="Bob")
        # await get_user_by_username(session=session, username="Nikola")
        await create_user_profile(
            session=session,
            user_id=user_bob.id,
            firstname="john",
        )


if __name__ == "__main__":
    asyncio.run(main())
