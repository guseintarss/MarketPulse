import re 
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator


LETER_MATCH_PATTERN = re.compile(r"^[a-яA-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:

        orm_mode = True



class ShowUser(TunedModel):
    user_id: uuid.UUID
    username: str
    surname: str
    email: EmailStr
    is_active: bool



class UserCreate(BaseModel):
    username: str
    surname: str
    email: EmailStr

    @validator("username")
    def validator_name(cls, value):
        if not LETER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validator_surename(cls, value):
        if not LETER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surename should contains only letters"
            )
        return value

