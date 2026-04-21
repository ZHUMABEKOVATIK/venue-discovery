import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Waynix", version="0.1.1")

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        port=8000
    )