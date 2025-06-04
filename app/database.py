from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion PostgreSQL (modifie si besoin : login/mdp/port/base)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:ouly03@localhost:5432/paye_ton_kawa"

# Création de l'engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création de la session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base commune pour tous les modèles
Base = declarative_base()
