from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from sqlalchemy import update, and_, select
from typing import Union
from uuid import UUID


class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, username: str, surname: str, email: str,
    ) -> User:
        new_user = User(
            username=username,
            surname=surname,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = update(User).\
            where(and_(User.user_id == user_id, User.is_active == True)).\
            values(is_active=False).\
            returning(User.user_id)
        res = await self.db_session.execute(query)
        delete_user_id_row = res.fetchone()
        if delete_user_id_row is not None:
            return delete_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def user_update(self, **kwargs) -> Union[User, None]:
        query = update(User).\
            where(User.is_active == True).\
            values(kwargs).\
            returning(User.user_id)

        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]
