import uvicorn
from fastapi import FastAPI

from src.api.v1 import v1_router
from src.middlewares import exception_handler_factory

app = FastAPI()

app.add_middleware(exception_handler_factory(app))
app.include_router(v1_router)


@app.get("/health")
def read_root():
    return {"message": "200 - OK"}


# Run the server using Uvicorn
if __name__ == "__main__":
    # print("I am in main")
    uvicorn.run(app, host="0.0.0.0", port=8000)
