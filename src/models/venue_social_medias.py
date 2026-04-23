from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, BigInteger

from src.db.base import IDMixIn

if TYPE_CHECKING:
    from .venue import Venue

class VenueSocialMedias(IDMixIn):
    __tablename__ = "venue_social_medias"

    venue_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    sm_type: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)

    venue: Mapped["Venue"] = relationship(back_populates="social_medias")