from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey

from src.db.base import IDMixIn

if TYPE_CHECKING:
    from .advertising import Advertising

class Category(IDMixIn):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("categories.id"))

    parent: Mapped["Category|None"] = relationship(remote_side="Category.id")
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
    ads: Mapped[list["Advertising"]] = relationship(back_populates="category")