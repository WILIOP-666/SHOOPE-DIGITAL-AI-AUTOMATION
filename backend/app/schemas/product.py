from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.product import ProductType

# Shared properties
class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    product_type: Optional[ProductType] = None
    content: Optional[str] = None
    is_active: Optional[bool] = True
    ai_enabled: Optional[bool] = False

# Properties to receive via API on creation
class ProductCreate(ProductBase):
    name: str
    price: float
    product_type: ProductType
    content: str

# Properties to receive via API on update
class ProductUpdate(ProductBase):
    pass

# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class ProductResponse(ProductInDBBase):
    pass
