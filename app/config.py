# app/config.py
import os
from pydantic import BaseModel

class Settings(BaseModel):
    DB_URL: str = os.getenv("DB_URL", "postgresql+psycopg2://postgres:postgres@db:5432/postgres")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "60"))

settings = Settings()
