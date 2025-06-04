from sqlalchemy.orm import Session
from app.models import Order
from app.schemas import OrderCreate


def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order(db: Session, order_id: int, new_data: OrderCreate):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        for field, value in new_data.dict().items():
            setattr(order, field, value)
        db.commit()
        db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return order

