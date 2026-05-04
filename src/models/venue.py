from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, BigInteger, Text, Numeric, Enum as SQLEnum, Integer

from src.db.base import SoftDeleteMixIn

if TYPE_CHECKING:
    from .model_enums import DataStatus
    from .user import User
    from .venue_social_medias import VenueSocialMedias
    from .region import Region
    from .category import Category
    from .feedback import Feedback
    from .visits import Visit
    from .venue_photos import VenuePhotos

class Venue(SoftDeleteMixIn):
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
    is_always_open: Mapped[bool] = mapped_column(Boolean, default=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    phone: Mapped[str | None] = mapped_column(String(20))

    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6))

    status: Mapped[DataStatus] = mapped_column(SQLEnum(DataStatus, name="venue_status"), default=DataStatus.new)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    visit_amount: Mapped[int] = mapped_column(Integer, default=0)
    promotion_percentage: Mapped[int] = mapped_column(Integer, default=5)

    # Relationships
    owner: Mapped["User"] = relationship(back_populates="venues")
    social_medias: Mapped[list["VenueSocialMedias"]] = relationship(back_populates="venue")
    region: Mapped["Region"] = relationship(back_populates="venues")
    category: Mapped["Category"] = relationship(foreign_keys=[category_id], back_populates="venues")
    subcategory: Mapped["Category"] = relationship(foreign_keys=[subcategory_id])
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="venue")
    visits: Mapped[list["Visit"]] = relationship(back_populates="venue")
    photos: Mapped[list["VenuePhotos"]] = relationship(back_populates="photos")