from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import func, DateTime
from datetime import datetime

import uuid

class Base(AsyncAttrs, DeclarativeBase):
    pass

class IDMixIn(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)

class TimeStampzMixIn(IDMixIn):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class SoftDeleteMixIn(TimeStampzMixIn):
    __abstract__ = True

    is_deleted: Mapped[bool] = mapped_column(default=False)
