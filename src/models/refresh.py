from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, UUID, DateTime, func, BigInteger

from src.db.base import TimeStampzMixIn
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class RefreshToken(TimeStampzMixIn):
    __tablename__ = "refresh_tokes"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
