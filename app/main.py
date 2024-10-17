from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import main_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(main_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Fiorino.AI API"}
