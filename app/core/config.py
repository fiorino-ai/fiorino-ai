
from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fiorino.AI"
    PROJECT_VERSION: str = "0.1.0"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://user:password@localhost/fiorino"  # Update this with your PostgreSQL credentials

    class Config:
        env_file = ".env"

settings = Settings()
