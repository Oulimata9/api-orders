from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas import OrderCreate, OrderOut
import requests
from app.event_bus import publish_event
import json
from datetime import datetime
from typing import List


router = APIRouter()

# URL MockAPI pour les commandes
ORDERS_URL = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/orders"

# Fonction pour convertir datetime en format JSON
def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type non sérialisable : {type(obj)}")

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate):
    print("ORDER REÇU :", order.dict())

    try:
        response = requests.post(
            ORDERS_URL,
            data=json.dumps(order.dict(), default=json_serial),
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        print("ERREUR :", e)
        raise HTTPException(status_code=500, detail="Erreur lors de l'envoi de la commande")

    if response.status_code != 201:
        print("ERREUR :", response.text)
        raise HTTPException(status_code=500, detail="Erreur lors de la création de la commande")

    created_order = response.json()
    publish_event(created_order)
    return created_order
    
@router.get("/", response_model=List[OrderOut])
def read_orders():
    response = requests.get(ORDERS_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des commandes")

    data = response.json()
    return data  # FastAPI fera la validation avec les alias


@router.get("/{order_id}", response_model=OrderOut)
def read_order(order_id: str):
    response = requests.get(f"{ORDERS_URL}/{order_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération de la commande")
    return response.json()

# NOUVELLE ROUTE : modifier une commande
@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: str, order: OrderCreate):
    print("MODIFICATION DEMANDÉE POUR :", order_id)
    try:
        payload = json.loads(json.dumps(order.dict(), default=json_serial))
    except Exception as e:
        print("Erreur JSON :", e)
        raise HTTPException(status_code=500, detail="Erreur de sérialisation JSON")

    response = requests.put(f"{ORDERS_URL}/{order_id}", json=payload)
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    if response.status_code != 200:
        print("ERREUR :", response.text)
        raise HTTPException(status_code=500, detail="Erreur lors de la modification de la commande")

    updated_order = response.json()
    publish_event(updated_order)
    return updated_order

@router.delete("/{order_id}")
def delete_order(order_id: str):
    # Vérifie si la commande existe
    response = requests.get(f"{ORDERS_URL}/{order_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    # Simule la suppression
    print(f"SIMULATION : Commande {order_id} supprimée")
    return {"message": f"Commande {order_id} (simulée comme supprimée)"}
