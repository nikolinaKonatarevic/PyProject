from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.base_model import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="User Email")
    password_hash: Mapped[str] = mapped_column(String, nullable=False, comment="User Hash Password")

    # relationships
    projects = relationship("Project", secondary="permissions", overlaps="project,permission")
    permissions = relationship("Permission", overlaps="projects,users")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
