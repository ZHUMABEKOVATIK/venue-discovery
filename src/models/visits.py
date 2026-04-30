from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger

from src.db.base import SoftDeleteMixIn

if TYPE_CHECKING:
    from .user import User
    from .venue import Venue

class Visit(SoftDeleteMixIn):
    __tablename__ = "visits"

    venue_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[int] = mapped_column(BigInteger, default=0)

    user: Mapped["User"] = relationship(back_populates="visits")
    venue: Mapped["Venue"] = relationship(back_populates="visits")