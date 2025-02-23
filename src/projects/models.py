from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from src.dataBase.base_model import Base
from src.documents.models import Document
from src.permissions.models import Permission
from src.users.models import User


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="Project Name")
    description: Mapped[str] = mapped_column(String, nullable=False, comment="Project Description")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_id"), nullable=False, comment="Foreign key to the User table - Owner"
    )

    # relationships
    owner: Mapped["User"] = relationship("User", back_populates="project")
    documents: Mapped[List["Document"]] = relationship(
        "Document", back_populates="project", cascade="all, delete-orphan"
    )
    premissions: Mapped[List["Permission"]] = relationship("Premission", back_populates="project")

    def __repr__(self):
        return f"<Project(name: {self.name})>"
