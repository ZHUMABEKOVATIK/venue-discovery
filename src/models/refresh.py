from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, DateTime, BigInteger

from src.db.base import TimeStampzMixIn
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class RefreshToken(TimeStampzMixIn):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user_agent : Mapped[str|None] = mapped_column(String(300), nullable=True)
    ip_address : Mapped[str|None] = mapped_column(String(50), nullable=True)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")