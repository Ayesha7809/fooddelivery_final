from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderOut
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.crud import order as crud_order
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_order = Order(
        user_id=current_user.id,
        restaurant_id=order.restaurant_id,
        total_amount=order.total_amount,
        status=order.status,
        payment_status=order.payment_status,
        food_item=order.food_item,
        quantity=order.quantity,
        delivery_address=order.delivery_address,
        ordered_by=current_user.username
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    orders = db.query(Order).all()
    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "restaurant_id": o.restaurant_id,
            "total_amount": o.total_amount,
            "status": o.status,
            "payment_status": o.payment_status,
            "food_item": o.food_item,
            "quantity": o.quantity,
            "delivery_address": o.delivery_address,
            "ordered_by": o.ordered_by
        }
        for o in orders
    ]



@router.put("/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int,
    order_update: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_type != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order fields
    for key, value in order_update.dict().items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_type != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"detail": f"Order {order_id} deleted"}
