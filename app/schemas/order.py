from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.order import OrderStatus

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    price: int
    product_id: int

    class Config:
        from_attributes=True

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: OrderStatus
    shipping_address: Optional[str]
    created_at: datetime
    user_id: int
    items = list[OrderItemResponse] = []

    class Config:
        from_attributes=True

class OrderCreate(BaseModel):
    shipping_address: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus