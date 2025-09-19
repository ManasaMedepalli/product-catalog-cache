# app/service.py
from typing import List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Product

def fetch_products_by_category(session: Session, category: str) -> List[Dict[str, Any]]:
    stmt = select(Product).where(Product.category == category)
    rows = session.execute(stmt).scalars().all()
    return [p.as_dict() for p in rows]

def get_products_service(session: Session, category: str) -> Tuple[list, dict]:
    """
    DB-only baseline: returns (items, meta)
    """
    items = fetch_products_by_category(session, category)
    meta = {
        "category": category,
        "source": "db",
        "cache_hit": False,
        "cache_key": f"products:{category}",
    }
    return items, meta
