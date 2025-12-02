from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from settings import Settings

# Cria o motor de conexão com o banco definido no .env
engine = create_engine(Settings().DATABASE_URL)

# Função que vai entregar uma sessão para cada rota da API usar
def get_session():
    with Session(engine) as session:
        yield session