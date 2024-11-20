from fastapi import APIRouter
from .v1 import v1_router
from app.core.config import settings

main_router = APIRouter()

@main_router.get("/")
async def health_check():
    return {
        "status": "ok",
        "version": settings.PROJECT_VERSION
    }

main_router.include_router(v1_router, prefix="/v1")
