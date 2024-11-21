from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import main_router
from fastapi.middleware.cors import CORSMiddleware
from app.static import admin

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, debug=settings.DEBUG)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Mount API routes
app.include_router(main_router, prefix="/api")

# Mount platform static files
admin.mount(app)