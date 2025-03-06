from src.documents import dto
from src.documents.repositories import DocumentRepository
from src.exceptions import (
    AccessDeniedException,
    DeleteFailedException,
    NotFoundException,
    PostFailedException,
    UpdateFailedException,
)
from src.permissions.enums import UserRole


class DocumentService:
    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    def get_all_documents(self, project_id: int, user_id: int) -> list[dto.Document]:
        if not self.repository.has_permission_proj(project_id, user_id, (UserRole.OWNER, UserRole.PARTICIPANT)):
            raise AccessDeniedException()

        documents = self.repository.get_all_documents(project_id)

        if not documents:
            raise NotFoundException()
        return [dto.Document.model_validate(doc) for doc in documents]

    def get_document(self, document_id: int, user_id: int) -> dto.Document:
        if not self.repository.has_permission_doc(document_id, user_id):
            raise AccessDeniedException()

        result = self.repository.get_document_by_doc_id(document_id)

        if not result:
            raise NotFoundException()
        return dto.Document.model_validate(result)

    def update_document(self, document_id: int, user_id: int, document_data: dto.DocumentUpdate) -> dto.Document:
        if not self.repository.get_document_by_doc_id(document_id):
            raise NotFoundException()

        if not self.repository.has_permission_doc(document_id, user_id):
            raise AccessDeniedException()

        result = self.repository.update_document(document_id, document_data.file_name, document_data.file_path)
        if result is None:
            raise UpdateFailedException()
        return dto.Document.model_validate(result)

    def delete_document(self, document_id: int, user_id: int) -> bool:
        if not self.repository.get_document_by_doc_id(document_id):
            raise NotFoundException()

        if not self.repository.has_permission_doc(document_id, user_id):
            raise AccessDeniedException()

        result = self.repository.delete_document(document_id)
        if not result:
            raise DeleteFailedException()
        return result

    def upload_documents(self, project_id: int, user_id: int, doc_data: list[dto.DocumentCreate]):
        if not self.repository.has_permission_proj(project_id, user_id, (UserRole.OWNER, UserRole.PARTICIPANT)):
            raise AccessDeniedException()

        result = self.repository.upload_documents(project_id, user_id, doc_data)
        if not result:
            raise PostFailedException()
        return [dto.Document.model_validate(project) for project in result]
