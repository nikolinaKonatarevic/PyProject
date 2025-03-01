from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data_base.base_model import Base
from src.permissions.models import Permission
from src.projects.models import Project


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="User Email")
    password: Mapped[str] = mapped_column(String, nullable=False, comment="User Password")

    # relationships
    projects: Mapped["Project"] = relationship("Project", back_populates="owner")
    permissions: Mapped["Permission"] = relationship("Permission", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
