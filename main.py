from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Product(Base):
    tablename = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    group = Column(String, default="")
    supplier = Column(String, default="")
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    variants = relationship("ProductVariant", back_populates="product")

class ProductVariant(Base):
    tablename = "product_variants"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float, default=0.0)
    quantity = Column(Integer, default=0)
    attributes = Column(JSON, default={})
    unit_of_measure = Column(String, default="unit")
    reorder_level = Column(Integer, default=5)
    location = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="variants")

# Admin table
class Admin(Base):
    tablename = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# لإنشاء الجداول
Base.metadata.create_all(bind=engine)
