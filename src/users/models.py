import uuid
from datetime import datetime
from typing import Type

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column

# Create Base and specify the type explicitly
Base: Type[DeclarativeMeta] = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        comment="Event ID - PK",
    )

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="User Email")

    password: Mapped[str] = mapped_column(String, nullable=False, comment="User Password")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="Account creation timestamp")

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now(), comment="Last updated timestamp"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
