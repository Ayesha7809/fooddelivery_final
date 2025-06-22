from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    total_amount = Column(Float)
    status = Column(String)
    payment_status = Column(String)
    food_item = Column(String)
    quantity = Column(Integer)
    delivery_address = Column(String)
    ordered_by = Column(String, nullable=False)

    user = relationship("User")
    restaurant = relationship("Restaurant")
