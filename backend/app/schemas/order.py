from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.order import OrderStatus

# Shared properties
class OrderBase(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = 1
    total_price: Optional[float] = None
    status: Optional[OrderStatus] = OrderStatus.PENDING
    shopee_order_id: Optional[str] = None
    delivery_data: Optional[str] = None
    is_delivered: Optional[bool] = False

# Properties to receive via API on creation
class OrderCreate(OrderBase):
    product_id: int
    total_price: float
    shopee_order_id: Optional[str] = None

# Properties to receive via API on update
class OrderUpdate(OrderBase):
    pass

# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class OrderResponse(OrderInDBBase):
    pass
