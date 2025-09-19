from sqlalchemy import Column, Integer, String, Numeric, DateTime, func, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": float(self.price),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Explicit index for faster category lookups
Index("idx_category", Product.category)
