from fastapi import UploadFile

from src.aws.s3 import S3Client
from src.documents import doc_dto
from src.documents.repositories import DocumentRepository
from src.exceptions import (
    AccessDeniedException,
    DeleteFailedException,
    NotFoundException,
    PostFailedException,
    UpdateFailedException,
)
from src.permissions.enums import UserRole
from src.users import dto

s3_client = S3Client()


class DocumentService:
    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    def get_all_documents(
        self, project_id: int, curr_user: dto.User, limit: int, offset: int
    ) -> doc_dto.PaginatedDocuments:
        if not self.repository.has_permission_proj(project_id, curr_user.id, (UserRole.OWNER, UserRole.PARTICIPANT)):
            raise AccessDeniedException()

        num_of_docs = self.repository.count_docs(project_id)

        if num_of_docs == 0:
            raise NotFoundException(message="No documents were found")

        documents = self.repository.get_all_documents(project_id)
        next_offset = offset + limit if offset + limit < num_of_docs else None
        prev_offset = max(0, offset - limit) if offset > 0 else None

        if not documents:
            raise NotFoundException()
        return doc_dto.PaginatedDocuments(documents=documents, count=num_of_docs, next=next_offset, prev=prev_offset)

    def download_document(self, document_id: int, curr_user: dto.User) -> doc_dto.Document:
        document = self.repository.has_permission_doc(document_id, curr_user.id)
        if not document:
            raise AccessDeniedException()

        result = s3_client.download(f"{document.file_name}", f"{document.file_path}")
        return result

    def update_document(self, document_id: int, curr_user: dto.User, document_updated: UploadFile) -> doc_dto.Document:
        if not self.repository.has_permission_doc(document_id, curr_user.id):
            raise AccessDeniedException()

        document = self.repository.get_document_by_doc_id(document_id)
        if not document:
            raise NotFoundException()

        s3_client.delete(f"{document.file_name}", f"{document.file_path}")
        url = s3_client.upload(document_updated, document.project_id, str(document.file_path))

        result = self.repository.update_document(document_id, document_updated.filename, document.file_path, url=url)
        if result is None:
            raise UpdateFailedException()
        return doc_dto.Document.model_validate(result)

    def delete_document(self, document_id: int, curr_user: dto.User) -> bool:
        if not self.repository.has_permission_doc(document_id, curr_user.id):
            raise AccessDeniedException()

        document = self.repository.get_document_by_doc_id(document_id)
        if not document:
            raise NotFoundException()

        s3_client.delete(f"{document.file_name}", f"{document.file_path}")

        result = self.repository.delete_document(document_id)
        if not result:
            raise DeleteFailedException()
        return result

    def upload_documents(
        self, project_id: int, curr_user: dto.User, doc_data: list[UploadFile]
    ) -> list[doc_dto.Document]:
        if not self.repository.has_permission_proj(project_id, curr_user.id, (UserRole.OWNER, UserRole.PARTICIPANT)):
            raise AccessDeniedException()

        document_urls = []

        for doc in doc_data:
            file_path = "documents"
            url = s3_client.upload(doc, project_id, file_path)
            document_urls.append(
                {"url": url, "file_name": doc.filename, "file_path": file_path, "content_type": doc.content_type}
            )

        result = self.repository.upload_documents(project_id, curr_user.id, document_urls)

        if not result:
            raise PostFailedException()
        return [doc_dto.Document.model_validate(project) for project in result]
