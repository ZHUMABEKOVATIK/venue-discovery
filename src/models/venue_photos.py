from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey, Integer

from src.db.base import IDMixIn

if TYPE_CHECKING:
    from .venue import Venue

class VenuePhotos(IDMixIn):
    __tablename__ = "venue_photos"

    venue_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    url: Mapped[str] = mapped_column(String)

    venue: Mapped["Venue"] = relationship(back_populates="photos")