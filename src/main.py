import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .core import general_settings, life_span
from .api import routers

app = FastAPI(title="Waynix", version="0.1.1", lifespan=life_span)

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

app.include_router(routers)
general_settings(app)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        port=8000
    )