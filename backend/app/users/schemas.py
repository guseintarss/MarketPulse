from typing import Annotated

from annotated_types import MaxLen
from annotated_types import MinLen
from pydantic import BaseModel
from pydantic import EmailStr

class CreateUser(BaseModel):
    username: Annotated[str, MaxLen(50), MinLen(3)]
    email: EmailStr
