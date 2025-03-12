from fastapi import APIRouter

from src.api.routers.v1.documents_routers import document_router
from src.api.routers.v1.projects_routers import project_router
from src.api.routers.v1.users_routers import user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user_router)
v1_router.include_router(project_router)
v1_router.include_router(document_router)
