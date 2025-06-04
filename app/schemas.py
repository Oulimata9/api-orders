from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Représente un produit commandé
class Product(BaseModel):
    name: str
    details: dict
    stock: int
    id: str
    orderId: str
    createdAt: Optional[datetime] = None

# Schéma d'entrée pour créer une commande
class OrderCreate(BaseModel):
    customer_id: Optional[str] = Field(..., alias="customerId")
    products: List[Product]

# Schéma de sortie pour afficher une commande
class OrderOut(OrderCreate):
    id: str
    createdAt: Optional[datetime]

