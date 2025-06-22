from pydantic import BaseModel

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str

class PaymentCreate(PaymentBase):
    pass

class PaymentOut(PaymentBase):
    id: int
    class Config:
        orm_mode = True