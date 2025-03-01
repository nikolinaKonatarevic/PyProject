from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data_base.base_model import Base
from src.projects.models import Project


class Document(Base):
    __tablename__ = "documents"

    file_name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="File name")
    file_path: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="File path")
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False, comment="Project ID")

    # relationships
    project: Mapped["Project"] = relationship("Project", back_populates="documents")

    def __repr__(self):
        return f"<Document(file name: {self.file_name})>"
