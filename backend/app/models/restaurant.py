from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    address = Column(String)
    phone = Column(String)