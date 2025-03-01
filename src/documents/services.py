from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.data_base.sync_engine import get_db_session
from src.documents import dto
from src.documents.models import Document
from src.documents.repositories import DocumentRepository


class DocumentService:
    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    def get_all_documents(self, project_id: int, user_id: int) -> List[dto.Document]:
        if not self.repository.has_permission_proj(project_id, user_id):
            raise HTTPException(
                status_code=403, detail=f"User with id {user_id} not authorized to access project with id {project_id}"
            )
        documents = self.repository.get_all_documents(project_id)
        if not documents:
            raise HTTPException(status_code=404, detail=f"Documents for project with id {project_id} do not exist")
        return [dto.Document.model_validate(doc) for doc in documents]

    def get_document(self, document_id: int, user_id: int) -> dto.Document:
        if not self.repository.has_permission_doc(document_id, user_id):
            raise HTTPException(
                status_code=403,
                detail=f"User with id {user_id} not authorized to access project that has doc with id {document_id}",
            )
        result = self.repository.get_document_by_doc_id(document_id)
        if not result:
            raise HTTPException(status_code=500)
        return dto.Document.model_validate(result)

    def update_document(self, document_id: int, user_id: int, document_data: dto.DocumentUpdate) -> dto.Document:
        if not self.repository.get_document_by_doc_id(document_id):
            raise HTTPException(status_code=404, detail=f"Docuemnt with id {document_id} is not found")

        if not self.repository.has_permission_doc(document_id, user_id):
            raise HTTPException(
                status_code=403,
                detail=f"User with id {user_id} not authorized to access project that has doc with id {document_id}",
            )

        result = self.repository.update_document(document_id, document_data.file_name, document_data.file_path)
        if result is None:
            raise HTTPException(status_code=404, detail="Updating document did not succeed")
        return dto.Document.model_validate(result)

    def delete_document(self, document_id: int, user_id: int) -> bool:
        if not self.repository.get_document_by_doc_id(document_id):
            raise HTTPException(status_code=404, detail=f"Docuemnt with id {document_id} is not found")

        if not self.repository.has_permission_doc(document_id, user_id):
            raise HTTPException(
                status_code=403,
                detail=f"User with id {user_id} not authorized to access project that has doc with id {document_id}",
            )

        result = self.repository.delete_document(document_id)
        return result

    def upload_documents(self, project_id: int, user_id: int, doc_data: List[dto.DocumentCreate]):
        if not self.repository.has_permission_proj(project_id, user_id):
            raise HTTPException(
                status_code=403, detail=f"User with id {user_id} not authorized to access project with id {project_id}"
            )

        def dto_to_model(dto_doc: dto.DocumentCreate) -> Document:
            doc_dict = dto_doc.model_dump()
            return Document(**doc_dict)

        doc_list = [dto_to_model(model) for model in doc_data]

        result = self.repository.upload_documents(project_id, user_id, doc_list)
        if not result:
            raise HTTPException(status_code=404, detail="Documents didn't upload successfully")
        return [dto.Document.model_validate(project) for project in result]


def get_document_service(db: Session = Depends(get_db_session)):
    repository = DocumentRepository(db)
    return DocumentService(repository)
