# seeds/seed.py
import random
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models import Base, Product
from app.db import engine, SessionLocal

CATEGORIES = ["shoes","electronics","books","toys","clothing","beauty","home","sports"]

def seed_products(total=2000, seed=42):
    # Ensure table exists (safe in dev)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Idempotent seeding: clear table and reset IDs
        db.execute("TRUNCATE TABLE products RESTART IDENTITY;")

        rng = random.Random(seed)
        batch = []
        for i in range(total):
            cat = rng.choice(CATEGORIES)
            price = Decimal(str(round(rng.uniform(5, 500), 2)))
            batch.append(Product(
                name=f"{cat.title()} Item {i+1}",
                category=cat,
                price=price
            ))

        db.bulk_save_objects(batch)
        db.commit()
        print(f"Seeded {total} products across {len(CATEGORIES)} categories.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
