from typing import Annotated

from annotated_types import MaxLen
from annotated_types import MinLen
from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr


class CreateUser(BaseModel):
    username: Annotated[str, MaxLen(50), MinLen(3)]
    email: EmailStr


class UserShema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    is_active: bool = True
