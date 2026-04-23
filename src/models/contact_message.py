from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean

from src.db.base import SoftDeleteMixIn

class ContactMessage(SoftDeleteMixIn):
    __tablename__ = "contact_messages"

    email: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)