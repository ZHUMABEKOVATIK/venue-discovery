from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey, Text

from src.db.base import TimeStampzMixIn

if TYPE_CHECKING:
    from .category import Category

class Advertising(TimeStampzMixIn):
    __tablename__ = "advertising"

    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    photo_url: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)

    category: Mapped["Category"] = relationship(back_populates="ads")