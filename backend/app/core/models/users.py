from pydantic.v1 import EmailStr
from sqlalchemy.orm import Mapped

from .base import Base


class Users(Base):
    __tablename__ = "users"

    username: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str]
    is_active: Mapped[bool]
