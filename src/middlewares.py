from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.exceptions import (
    AccessDeniedException,
    DeleteFailedException,
    NotFoundException,
    PostFailedException,
    UpdateFailedException,
)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    def dispatch(self, request: Request, call_next):
        try:
            return call_next(request)
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client Error", "message": str(http_exception.detail)},
            )
        except NotFoundException as e:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "Client Error", "message": str(e.message)},
            )
        except AccessDeniedException as e:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"error": "Client Error", "message": str(e.message)},
            )
        except PostFailedException as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error", "message": str(e.message)},
            )
        except UpdateFailedException as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error", "message": str(e.message)},
            )
        except DeleteFailedException as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error", "message": str(e.message)},
            )
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
            )
