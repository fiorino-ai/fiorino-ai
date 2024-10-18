from pydantic.v1 import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fiorino.AI"
    PROJECT_VERSION: str = "0.1.0"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://user:password@localhost/fiorino"  # Update this with your PostgreSQL credentials

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]  # Allow all origins by default
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]  # Allow all methods
    CORS_ALLOW_HEADERS: List[str] = ["*"]  # Allow all headers

    class Config:
        env_file = ".env"

settings = Settings()
