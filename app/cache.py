# app/cache.py
import json
import redis
from typing import Any, Optional, Tuple
from app.config import settings

# Single shared client (decode_responses=True -> store/read strings)
_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_json(key: str) -> Optional[Any]:
    raw = _client.get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # If cache got corrupted somehow, treat as miss
        return None

def set_json(key: str, value: Any, ttl_seconds: int) -> None:
    payload = json.dumps(value, ensure_ascii=False)
    # setex = set with TTL
    _client.setex(key, ttl_seconds, payload)

def delete(key: str) -> None:
    _client.delete(key)

def ping_redis() -> Tuple[bool, str]:
    try:
        ok = _client.ping()
        return (bool(ok), "pong" if ok else "no-pong")
    except Exception as e:
        return (False, str(e))
