# app/service.py
from typing import List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Product
from app.config import settings
from app.cache import get_json, set_json

def fetch_products_by_category(session: Session, category: str) -> List[Dict[str, Any]]:
    stmt = select(Product).where(Product.category == category)
    rows = session.execute(stmt).scalars().all()
    return [p.as_dict() for p in rows]

def get_products_service(session: Session, category: str, db_only: bool = False) -> Tuple[list, dict]:
    """
    Returns (items, meta). If caching is enabled and db_only is False,
    uses cache-aside with key 'products:{category}' and TTL from settings.
    """
    cache_key = f"products:{category}"

    # If cache is enabled and not forcing DB path, try cache first
    if settings.CACHE_ENABLED and not db_only:
        cached = get_json(cache_key)
        if cached is not None:
            meta = {
                "category": category,
                "source": "cache",
                "cache_hit": True,
                "cache_key": cache_key,
            }
            return cached, meta

        # Miss -> fetch from DB, then populate cache
        items = fetch_products_by_category(session, category)
        set_json(cache_key, items, settings.CACHE_TTL_SECONDS)
        meta = {
            "category": category,
            "source": "db",
            "cache_hit": False,
            "cache_key": cache_key,
        }
        return items, meta

    # Cache disabled or db_only=True -> always DB
    items = fetch_products_by_category(session, category)
    meta = {
        "category": category,
        "source": "db",
        "cache_hit": False,
        "cache_key": cache_key,
    }
    return items, meta

