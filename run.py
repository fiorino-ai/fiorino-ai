import uvicorn
from app.core.config import settings
from yoyo import read_migrations
from yoyo import get_backend

def apply_migrations():
    backend = get_backend(settings.DATABASE_URL)
    migrations = read_migrations('./migrations')
     
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

if __name__ == "__main__":
    apply_migrations()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
