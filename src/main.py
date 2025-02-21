import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def read_root():
    return {"message": "200 - OK"}


# Run the server using Uvicorn
if __name__ == "__main__":
    # print("I am in main")
    uvicorn.run(app, host="0.0.0.0", port=8000)
