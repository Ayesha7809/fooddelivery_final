from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_handler import decode_access_token  
from passlib.context import CryptContext
from app.models.user import User
from sqlalchemy.orm import Session


# ✅ Only define JWTBearer once
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            try:
                payload = decode_access_token(credentials.credentials)
                return payload
            except Exception as e:
                raise HTTPException(status_code=403, detail=f"Invalid or expired token: {str(e)}")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


# 🔐 Password utils
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
