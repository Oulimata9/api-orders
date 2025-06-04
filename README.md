# API Orders – PayeTonKawa ☕️

Microservice de gestion des commandes pour la plateforme e-commerce PayeTonKawa, développé dans le cadre de la MSPR TPRE814.

## Description

Cette API permet de gérer l'ensemble des opérations liées aux **commandes clients** :

- Création d'une commande
- Consultation de commandes
- Modification ou suppression
- Liaison avec les clients et les produits
- Communication asynchrone via RabbitMQ (Event-Driven)

## Technologies utilisées

- **Python 3.11**
- **FastAPI** – Framework REST
- **Pydantic** – Validation des données
- **Uvicorn** – Serveur ASGI
- **RabbitMQ** – Message broker (asynchrone)
- **Pika** – Client Python RabbitMQ
- **Docker** – Conteneurisation
- **Pytest** – Tests unitaires
- **GitHub Actions** – Intégration continue

## Installation

### En local

```bash
git clone https://github.com/Oulimata9/api-orders.git
cd api-orders
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt


## Lancer l'API

uvicorn app.main:app --reload

## RabbitMQ via Docker
 
docker run -d --hostname rabbit --name rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management

Interface RabbitMQ : http://localhost:15672
(login : guest, mot de passe : guest)

## Événements RabbitMQ
L’API publie des messages RabbitMQ à chaque création ou modification de commande :

Événement                  Queue
Commande créée             order_created
Commande modifiée          order_updated

## Structure du projet

api-orders/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routes/orders.py
│   └── event_bus.py
├── tests/
│   └── test_orders.py
├── requirements.txt
├── Dockerfile
├── README.md
└── postman/
    ├── api-orders.postman_collection.json
    └── api-orders.postman_environment.json


## Auteur
Projet réalisé par Oulimata dans le cadre de la MSPR TPRE814.

