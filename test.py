from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, table_registry


app = FastAPI(title='API de teste')

engine = create_engine("sqlite:///:memory:", echo=True)

table_registry.metadata.create_all(engine)


with Session(engine) as session:
    print("--- Criando utilizador ---")
    mairon = User(
        username="mairon", password="senha123", email="mairon@email.com"
    )

    session.add(mairon)
    session.commit()  
    session.refresh(mairon)  

    print("\n--- DADOS DO UTILIZADOR ---")
    print("DADOS COMPLETOS:", mairon)
    print("ID:", mairon.id)
    print("Criado em:", mairon.created_at)
    print("----------------------------")