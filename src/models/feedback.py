from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey, Integer

from src.db.base import SoftDeleteMixIn

if TYPE_CHECKING:
    from .venue import Venue

class Feedback(SoftDeleteMixIn):
    __tablename__ = "feedbacks"

    venue_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String)

    venue: Mapped["Venue"] = relationship(back_populates="feedbacks")
