from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from .base import Base

if TYPE_CHECKING:
    from .profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(55), unique=True)
    email: Mapped[str | None]
    password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=sa.text("true")
    )

    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
