from typing import Annotated

from fastapi import APIRouter, Depends, Query, UploadFile
from starlette import status

from src.deps import get_document_service
from src.documents import doc_dto
from src.documents.services import DocumentService
from src.users import dto
from src.users.user_deps import get_curr_user

document_router = APIRouter(tags=["documents"])


@document_router.get("/projects/{project_id}/documents", status_code=status.HTTP_200_OK)
def get_all_documents(
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    project_id: int,
    document_service: DocumentService = Depends(get_document_service),
    limit: int = Query(5, ge=1, le=10, title="Limit"),
    offset: int = Query(0, ge=0, title="Offset"),
) -> doc_dto.PaginatedDocuments:
    return document_service.get_all_documents(project_id, curr_user, limit, offset)


@document_router.post("/projects/{project_id}/documents", status_code=status.HTTP_201_CREATED)
def upload_documents(
    project_id: int,
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    doc_data: list[UploadFile],
    document_service: DocumentService = Depends(get_document_service),
) -> list[doc_dto.Document]:
    return document_service.upload_documents(project_id, curr_user, doc_data)


@document_router.get("/document/{document_id}", status_code=status.HTTP_200_OK)
def download_document(
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    document_id: int,
    document_service: DocumentService = Depends(get_document_service),
):
    return document_service.download_document(document_id, curr_user)


@document_router.patch("/document/{document_id}", status_code=status.HTTP_200_OK)
def update_document(
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    document_id: int,
    document_updated: UploadFile,
    document_service: DocumentService = Depends(get_document_service),
) -> doc_dto.Document:
    return document_service.update_document(document_id, curr_user, document_updated)


@document_router.delete("/document/{document_id}")
def delete_document(
    curr_user: Annotated[dto.User, Depends(get_curr_user)],
    document_id: int,
    document_service: DocumentService = Depends(get_document_service),
) -> bool:
    return document_service.delete_document(document_id, curr_user)
