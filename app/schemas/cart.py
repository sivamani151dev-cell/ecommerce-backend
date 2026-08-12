from pydantic import BaseModel
from typing import Optional

class CartItemResponse(BaseModel):
    id: int
    quantity: int
    product_id : int
    cart_id : int

    class Config: 
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id : int
    items : list[CartItemResponse] = []

    class Config:
        from_attributes = True

class AddToCart(BaseModel):
    quantity: int = 1