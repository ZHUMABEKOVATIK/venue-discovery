import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .core import general_settings, life_span
from .api import routers

app = FastAPI(title="Waynix", version="0.1.1", lifespan=life_span)
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(routers)
general_settings(app)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        port=8000
    )