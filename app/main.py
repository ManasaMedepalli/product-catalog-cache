from fastapi import FastAPI
from sqlalchemy import text
from app.models import Base
from app.db import engine
from app.config import settings
import redis

app = FastAPI(title="Product Catalog Cache v0.1")

@app.on_event("startup")
def startup():
    # Dev-only: ensure tables exist
    Base.metadata.create_all(bind=engine)

def ping_redis():
    try:
        r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        return r.ping()
    except Exception:
        return False

@app.get("/health")
def health():
    # Check DB
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "status": "ok" if db_ok else "degraded",
        "db": db_ok,
        "cache": ping_redis(),
        "cache_enabled": settings.CACHE_ENABLED,
    }
