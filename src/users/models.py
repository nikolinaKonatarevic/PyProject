from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_model import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="User Email")
    password: Mapped[str] = mapped_column(String, nullable=False, comment="User Password")

    # relationships
    projects = relationship("Project", back_populates="users")
    permissions = relationship("Permission", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
