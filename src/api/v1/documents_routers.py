from fastapi import APIRouter, Depends
from starlette import status

from src.deps import get_document_service
from src.documents import dto
from src.documents.services import DocumentService

document_router = APIRouter(tags=["documents"])


@document_router.get("/documents", status_code=status.HTTP_200_OK)
def get_all_documents(
    user_id: int, project_id: int, document_service: DocumentService = Depends(get_document_service)
) -> list[dto.Document]:
    return document_service.get_all_documents(project_id, user_id)


@document_router.post("/documents", status_code=status.HTTP_201_CREATED)
def upload_documents(
    project_id: int,
    user_id: int,
    doc_data: list[dto.DocumentCreate],
    document_service: DocumentService = Depends(get_document_service),
) -> list[dto.Document]:
    return document_service.upload_documents(project_id, user_id, doc_data)


@document_router.get("/document/{document_id}", status_code=status.HTTP_200_OK)
def get_document_by_id(
    user_id: int, document_id: int, document_service: DocumentService = Depends(get_document_service)
) -> dto.Document:
    return document_service.get_document(document_id, user_id)


@document_router.patch("/document/{document_id}", status_code=status.HTTP_200_OK)
def update_document(
    user_id: int,
    document_id: int,
    document_data: dto.DocumentUpdate,
    document_service: DocumentService = Depends(get_document_service),
) -> dto.Document:
    return document_service.update_document(document_id, user_id, document_data)


@document_router.delete("/document/{document_id}")
def delete_document(
    user_id: int,
    document_id: int,
    document_service: DocumentService = Depends(get_document_service),
) -> bool:
    return document_service.delete_document(document_id, user_id)
