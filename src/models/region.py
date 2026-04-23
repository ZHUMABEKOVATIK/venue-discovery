from typing import TYPE_CHECKING
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Enum as SQLEnum

from src.db.base import IDMixIn

if TYPE_CHECKING:
    from .venue import Venue

class Region(IDMixIn):
    __tablename__ = "regions"

    name: Mapped[str] = mapped_column(String)

    venues: Mapped[list["Venue"]] = relationship(back_populates="region")