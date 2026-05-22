from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from typing import TYPE_CHECKING
from .mixin import UserRelationMixin
from .base import Base

if TYPE_CHECKING:
    from .user import User


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"
    firstname: Mapped[str | None] = mapped_column(String(55))
    lastname: Mapped[str | None] = mapped_column(String(55))
    age: Mapped[int | None]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
