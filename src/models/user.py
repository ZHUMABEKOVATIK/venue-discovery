from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Enum as SQLEnum

from src.db.base import SoftDeleteMixIn

if TYPE_CHECKING:
    from .venue import Venue
    from .announcement import Announcement
    from .visits import Visit
    from .model_enums import UserRole
    from .feedback import Feedback
    from .refresh import RefreshToken

class User(SoftDeleteMixIn):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_pw: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="user_role"), default=UserRole.guest)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    venues: Mapped[list["Venue"]] = relationship(back_populates="owner")
    announcements: Mapped[list["Announcement"]] = relationship(back_populates="user")
    visits: Mapped[list["Visit"]] = relationship(back_populates="user")
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="user")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")