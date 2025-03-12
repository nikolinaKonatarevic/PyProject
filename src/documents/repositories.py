from sqlalchemy import Delete, Insert, Select, Update, delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.documents.models import Document
from src.exceptions import PostFailedException
from src.permissions.enums import UserRole
from src.permissions.models import Permission
from src.projects.models import Project


class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_document_by_doc_id(self, document_id: int) -> Document | None:
        """Get one document by id"""
        query: Select = select(Document).where(Document.id == document_id)

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_all_documents(self, project_id: int) -> list[Document] | None:
        """Executing query for getting all documents"""
        query: Select = select(Document).where(Document.project_id == project_id)

        result = self.session.execute(query)
        projects = list(result.scalars().all())
        return projects if projects else None

    def create_document(self, project_id: int, file_name: str, file_path: str) -> Document | None:
        """Inserts a new document and returns the created Document object"""
        query: Insert = (
            insert(Document).values(project_id=project_id, file_name=file_name, file_path=file_path).returning(Document)
        )

        try:
            result = self.session.execute(query)
            return result.scalar_one_or_none()
        except IntegrityError:
            raise PostFailedException("Unsuccessful creation of document in db")

    def upload_documents(self, project_id: int, user_id: int, doc_data: list) -> list[Document] | None:
        """Uploads one or more documents in one transaction."""
        if not doc_data:
            return None

        documents = [
            {"project_id": project_id, "file_name": doc["file_name"], "file_path": doc["file_path"], "url": doc["url"]}
            for doc in doc_data
        ]

        query: Insert = insert(Document).values(documents).returning(Document)

        result = self.session.execute(query)
        if result:
            self.session.commit()
        self.session.rollback()
        return list(result.scalars().all()) if result else None

    def update_document(self, document_id: int, file_name: str, file_path: str, url: str) -> Document | None:
        """Updates a document by ID and returns True if updated, False if not found."""
        query: Update = (
            update(Document).where(Document.id == document_id).values(file_name=file_name, file_path=file_path, url=url)
        )

        result = self.session.execute(query)
        self.session.commit()
        return result.scalar_one_or_none()

    def delete_document(self, document_id: int) -> bool:
        """Deletes a document by ID and returns True if deleted, False otherwise."""
        query: Delete = delete(Document).where(Document.id == document_id)

        result = self.session.execute(query)

        if result.fetchone() > 0:
            self.session.commit()
            return True
        return False

    def has_permission_doc(self, document_id, user_id):
        query: Select = (
            select(Document)
            .join(Project, Project.id == Document.project_id)
            .join(Permission, Permission.project_id == Project.id)
            .where(
                Document.id == document_id,
                Permission.user_id == user_id,
                Permission.user_role.in_((UserRole.OWNER, UserRole.PARTICIPANT)),
            )
        )

        result = self.session.execute(query)
        return result.scalar() is not None

    def has_permission_proj(self, project_id: int, curr_user_id: int, roles: tuple[UserRole, ...]) -> bool:
        query: Select = select(Permission).where(
            Permission.project_id == project_id, Permission.user_id == curr_user_id
        )

        if roles:
            query = query.where(Permission.user_role.in_(roles))

        result = self.session.execute(query)
        return result.scalar() is not None

    def count_docs(self, project_id: int) -> int:
        query = select(func.count()).select_from(Document).where(Document.project_id == project_id)
        result = self.session.execute(query).scalar()
        return result
