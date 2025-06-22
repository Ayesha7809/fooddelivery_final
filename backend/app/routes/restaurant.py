from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.restaurant import RestaurantCreate, RestaurantOut
from app.crud import restaurant as crud_restaurant
from typing import List
from fastapi import HTTPException


router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RestaurantOut)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    return crud_restaurant.create_restaurant(db, restaurant)

@router.get("/", response_model=List[RestaurantOut])
def read_restaurants(db: Session = Depends(get_db)):
    return crud_restaurant.get_restaurants(db)


@router.put("/{restaurant_id}", response_model=RestaurantOut)
def update_restaurant(restaurant_id: int, restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    updated = crud_restaurant.update_restaurant(db, restaurant_id, restaurant)
    if not updated:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return updated

@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    deleted = crud_restaurant.delete_restaurant(db, restaurant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Restaurant deleted successfully"}
