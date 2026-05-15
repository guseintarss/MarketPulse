from typing import Annotated

from fastapi import FastAPI, Depends

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


app = FastAPI()



engine = create_async_engine("sqlite+aiosqlite:///users_user.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with  new_session() as session:
        yield session 


SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str]

@app.post("/setup_database")
async def setup_databse():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}

class UserRegSchema(BaseModel):
    username: str
    password: str 

class UserSchema(UserRegSchema):
    id: int

@app.post("/users")
async def reg_user(data: UserRegSchema, session: SessionDep):
    new_user = UserModel(
        username=data.username,
        password=data.password,
    )
    session.add(new_user)
    await session.commit()
    return {"OK": True} 
    

@app.get("/get_user")
async def get_user(session: SessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()

    
