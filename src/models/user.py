from typing import TYPE_CHECKING
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Enum as SQLEnum

from src.db.base import SoftDeleteMixIn

if TYPE_CHECKING:
    from .venue import Venue

class UserRole(PyEnum, str):
    guest = "guest"
    owner = "owner"
    admin = "admin"

class User(SoftDeleteMixIn):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_pw: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="user_role"), default=UserRole.guest)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    venues: Mapped[list["Venue"]] = relationship(back_populates="owner")