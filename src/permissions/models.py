from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from src.database.base_model import Base
from src.permissions.enums import RequestStatus, UserRole


class Permission(Base):
    __tablename__ = "permissions"

    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False, comment="Project ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="User ID")
    user_role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, comment="User Role")
    request_status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus), nullable=False, comment="Request Status")

    # relationships
    user = relationship("User", back_populates="permissions")
    project = relationship("Project", back_populates="permissions")

    def __repr__(self):
        return f"<Permission(project id = {self.id}, user id ={self.user_id})>"
