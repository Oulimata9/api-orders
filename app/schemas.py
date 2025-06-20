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
    customer_id: str = Field(..., alias="customerId")
    products: List[Product]

    class Config:
        populate_by_name = True

# Schéma de sortie pour afficher une commande
class OrderOut(BaseModel):
    customer_id: str = Field(..., alias="customerId")
    products: List[Product]
    id: str
    createdAt: Optional[datetime]

    class Config:
        populate_by_name = True
