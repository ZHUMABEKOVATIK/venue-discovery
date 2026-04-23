from typing import TYPE_CHECKING
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, BigInteger, Text, Numeric, Enum as SQLEnum

from src.db.base import TimeStampzMixIn

if TYPE_CHECKING:
    from .user import User
    from .venue_social_medias import VenueSocialMedias
    from .region import Region
    from .category import Category
    from .feedback import Feedback

class VenueStatus(PyEnum, str):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected" 
    revision = "revision"

class Venue(TimeStampzMixIn):
    __tablename__ = "venues"

    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name_kr: Mapped[str | None] = mapped_column(String(200))
    name_uz: Mapped[str | None] = mapped_column(String(200))
    name_ru: Mapped[str | None] = mapped_column(String(200))
    name_en: Mapped[str | None] = mapped_column(String(200))

    description_kr: Mapped[str | None] = mapped_column(Text)
    description_uz: Mapped[str | None] = mapped_column(Text)
    description_ru: Mapped[str | None] = mapped_column(Text)
    description_en: Mapped[str | None] = mapped_column(Text)

    address_kr: Mapped[str | None] = mapped_column(String(300))
    address_uz: Mapped[str | None] = mapped_column(String(300))
    address_ru: Mapped[str | None] = mapped_column(String(300))
    address_en: Mapped[str | None] = mapped_column(String(300))

    region_id: Mapped[int | None] = mapped_column(ForeignKey("regions.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    subcategory_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    day_of_week: Mapped[int | None] = mapped_column(BigInteger)
    open_time: Mapped[str | None] = mapped_column(String(5))
    close_time: Mapped[str | None] = mapped_column(String(5))
    is_24_7: Mapped[bool] = mapped_column(Boolean, default=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    phone: Mapped[str | None] = mapped_column(String(20))

    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6))

    status: Mapped[VenueStatus] = mapped_column(SQLEnum(VenueStatus, name="venue_status"), default=VenueStatus.pending)
    comment: Mapped[str: None] = mapped_column(Text, nullable=True)

    # Relationships
    owner: Mapped["User"] = relationship(back_populates="venues")
    social_medias: Mapped[list["VenueSocialMedias"]] = relationship(back_populates="venue")
    region: Mapped["Region"] = relationship(back_populates="venues")
    category: Mapped["Category"] = relationship(foreign_keys=[category_id], back_populates="")
    subcategory: Mapped["Category"] = relationship(foreign_keys=[subcategory_id])
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="venue")