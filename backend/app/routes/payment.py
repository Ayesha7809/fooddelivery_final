from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.payment import PaymentCreate, PaymentOut
from app.crud import payment as crud_payment
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_db
from app.models.payment import Payment
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/payments", tags=["Payments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PaymentOut)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return crud_payment.create_payment(db, payment)

@router.get("/", response_model=List[PaymentOut])
def read_payments(db: Session = Depends(get_db)):
    return crud_payment.get_payments(db)

@router.post("/", response_model=PaymentOut)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.user_type != "user":
        raise HTTPException(status_code=403, detail="Only users can make payments")

    new_payment = Payment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/", response_model=List[PaymentOut])
def get_all_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view payments")

    return db.query(Payment).all()