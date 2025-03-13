from fastapi import Depends
from sqlalchemy.orm import Session

from src.api.aws.s3 import S3Client
from src.api.database.sync_engine import get_db_session
from src.api.documents.repositories import DocumentRepository
from src.api.documents.services import DocumentService
from src.api.projects.repositories import ProjectRepository
from src.api.projects.services import ProjectService
from src.api.users.repositories import UserRepository
from src.api.users.services import UserService


def get_s3_client() -> S3Client:
    s3_client = S3Client()
    return s3_client


def get_document_service(db: Session = Depends(get_db_session)):
    repository = DocumentRepository(db)
    return DocumentService(repository)


def get_project_service(db: Session = Depends(get_db_session)):
    repository = ProjectRepository(db)
    return ProjectService(repository)


def get_user_service(db: Session = Depends(get_db_session)):
    repository = UserRepository(db)
    return UserService(repository)
