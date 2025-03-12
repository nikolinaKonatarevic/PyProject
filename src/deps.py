from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.sync_engine import get_db_session
from src.documents.repositories import DocumentRepository
from src.documents.services import DocumentService
from src.projects.repositories import ProjectRepository
from src.projects.services import ProjectService
from src.users.repositories import UserRepository
from src.users.services import UserService


def get_document_service(db: Session = Depends(get_db_session)):
    repository = DocumentRepository(db)
    return DocumentService(repository)


def get_project_service(db: Session = Depends(get_db_session)):
    repository = ProjectRepository(db)
    return ProjectService(repository)


def get_user_service(db: Session = Depends(get_db_session)):
    repository = UserRepository(db)
    return UserService(repository)
