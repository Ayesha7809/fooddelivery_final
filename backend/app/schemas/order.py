from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    restaurant_id: int
    total_amount: float
    status: str
    payment_status: str
    food_item: str
    quantity: int
    delivery_address: str

# ❌ REMOVE ordered_by from OrderCreate
class OrderCreate(OrderBase):
    pass

# ✅ KEEP ordered_by in OrderOut for display
class OrderOut(OrderBase):
    id: int
    user_id: int
    ordered_by: str  # Only in response
    class Config:
        orm_mode = True
