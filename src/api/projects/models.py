from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from src.api.database.base_model import Base


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="Project Name")
    description: Mapped[str] = mapped_column(String, nullable=False, comment="Project Description")
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, comment="Foreign key to the User table - Owner"
    )

    # relationships
    owner = relationship("User")
    documents = relationship("Document", backref="projects")
    users = relationship("User", secondary="permissions", back_populates="projects", overlaps="permissions")
    permissions = relationship("Permission", overlaps="users")

    def __repr__(self):
        return f"<Project(name: {self.name})>"
