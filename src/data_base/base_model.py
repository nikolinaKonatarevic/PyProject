from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())
