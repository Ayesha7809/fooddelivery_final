from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from pydantic import BaseModel
from passlib.hash import bcrypt
from typing import List
from app.schemas.user import UserOut
from app.dependencies.auth import get_current_user, admin_only

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    user_type: str

class UserUpdate(BaseModel):
    email: str = None
    password: str = None
    user_type: str = None


# ✅ Register New User
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = bcrypt.hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        user_type=user.user_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


# ✅ Get All Users - Admin only
@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return db.query(User).all()


# ✅ Update User - Admin only
@router.put("/{user_id}")
def update_user(user_id: int, update: UserUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update.email:
        user.email = update.email
    if update.user_type:
        user.user_type = update.user_type
    if update.password:
        user.hashed_password = bcrypt.hash(update.password)

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully"}


# ✅ Delete User - Admin only
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
