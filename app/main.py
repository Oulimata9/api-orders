from fastapi import FastAPI
from app import routes
from app.database import Base, engine

# Création des tables en base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Microservice",
    description="Microservice de gestion des commandes pour le MSPR",
    version="1.0.0"
)

# Inclusion des routes de l'API
app.include_router(routes.router, prefix="/orders", tags=["Orders"])
 