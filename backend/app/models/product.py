from sqlalchemy import Boolean, Column, Integer, String, Float, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base

class ProductType(str, enum.Enum):
    TEMPLATE = "template"
    ACCOUNT = "account"
    LINK = "link"
    VOUCHER = "voucher"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    product_type = Column(Enum(ProductType), nullable=False)
    content = Column(Text)  # Template content, account details, link, or voucher code
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    ai_enabled = Column(Boolean, default=False)  # Whether AI is enabled for this product
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", back_populates="products")
    orders = relationship("Order", back_populates="product")
