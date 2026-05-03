from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger, Enum as SQLEnum, Text, String

from src.db.base import SoftDeleteMixIn

if TYPE_CHECKING:
    from .model_enums import DataStatus
    from .user import User

class Announcement(SoftDeleteMixIn):
    __tablename__ = "announcements"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    photo_url: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[DataStatus] = mapped_column(SQLEnum(DataStatus, name="announcement_status"), default=DataStatus.pending)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="announcements")