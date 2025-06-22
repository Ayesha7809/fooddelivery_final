from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.token import Token
from datetime import datetime, timedelta
from jose import jwt
router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={
        "sub": user.username,
        "user_type": user.user_type,
        "user_id": user.id
})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.user_type  # ✅ THIS IS WHAT'S MISSING!
    }





SECRET_KEY = "your_secret"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
