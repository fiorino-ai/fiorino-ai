from pydantic.v1 import BaseSettings
from typing import List
from app.core.version import __version__

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fiorino.AI"
    PROJECT_VERSION: str = __version__
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://user:password@localhost/fiorino"

    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
