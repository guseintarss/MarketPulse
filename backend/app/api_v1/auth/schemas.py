from pydantic import BaseModel, ConfigDict
from typing import Annotated
from annotated_types import MaxLen, MinLen


class RegisterUser(BaseModel):
    username: Annotated[str, MaxLen(50), MinLen(3)]
    email: str
    password: Annotated[str, MinLen(4)]
    is_active: bool = True


class UserLogin(BaseModel):
    username: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str | None
    is_active: bool
