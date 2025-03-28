import uvicorn
from fastapi import FastAPI

from src.api.middlewares import ExceptionHandlerMiddleware
from src.api.routers.v1 import v1_router

app = FastAPI()

app.add_middleware(ExceptionHandlerMiddleware)  # type = ignore
app.include_router(v1_router)


@app.get("/health")
def read_root():
    return {"message": "200 - OK"}


# Run the server using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
