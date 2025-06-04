from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    products = Column(JSON)
