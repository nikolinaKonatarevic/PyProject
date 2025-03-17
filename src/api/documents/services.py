from fastapi import UploadFile
import random
from src.api.aws.s3 import S3Client
from src.api.documents import dto as doc_dto
from src.api.documents.repositories import DocumentRepository
from src.api.exceptions import (
    AccessDeniedException,
    DeleteFailedException,
    NotFoundException,
    PostFailedException,
    UpdateFailedException,
)
from src.api.permissions.enums import UserRole
from src.api.users import dto


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

    def download_document(self, document_id: int, curr_user: dto.User, s3_client: S3Client) -> doc_dto.Document:
        document = self.repository.has_permission_doc(document_id, curr_user.id)
        if not document:
            raise AccessDeniedException()

        result = s3_client.download(f"{document.file_name}", f"{document.file_path}")
        return result

    def update_document(
        self, document_id: int, curr_user: dto.User, document_updated: UploadFile, s3_client: S3Client
    ) -> doc_dto.Document:
        if not self.repository.has_permission_doc(document_id, curr_user.id):
            raise AccessDeniedException()

        document = self.repository.get_document_by_doc_id(document_id)
        if not document:
            raise NotFoundException()

        s3_client.delete(f"{document.file_name}", f"{document.file_path}")
        random_number = random.randint(10000, 99999)
        document_updated.filename = f"{random_number}_{document_updated.filename}"

        url = s3_client.upload(document_updated, str(document.file_path))

        result = self.repository.update_document(document_id, document_updated.filename, document.file_path, url=url)
        if result is None:
            raise UpdateFailedException()
        return doc_dto.Document.model_validate(result)

    def delete_document(self, document_id: int, curr_user: dto.User, s3_client: S3Client) -> bool:
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
        self, project_id: int, curr_user: dto.User, doc_data: list[UploadFile], s3_client: S3Client
    ) -> list[doc_dto.Document]:
        if not self.repository.has_permission_proj(project_id, curr_user.id, (UserRole.OWNER, UserRole.PARTICIPANT)):
            raise AccessDeniedException()

        documents_list = []
        file_path = "unproccessed"

        for doc in doc_data:
            random_number = random.randint(10000, 99999)
            doc.filename = f"{random_number}_{doc.filename}"
            url = s3_client.upload(doc, file_path)
            document_info = {"file_name": doc.filename, "file_path": file_path, "url": url}
            documents_list.append(document_info)

        result = self.repository.upload_documents(project_id, curr_user.id, documents_list)

        if not result:
            for doc in doc_data:
                s3_client.delete(doc.filename, file_path)
            raise PostFailedException()
        return [doc_dto.Document.model_validate(project) for project in result]
