from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_session
from models import User
from schema import UsuarioPublic, BaseUsuario, Usuario  # Certifique-se que seu arquivo é 'schema.py' ou 'schemas.py'

app = FastAPI(title='API de receitas')

# --- ROTAS DE USUÁRIOS ---

@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(user: BaseUsuario, session: Session = Depends(get_session)):
    # Verifica se username ou email já existem
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome de usuário já existe'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email já existe'
            )

    # Cria o usuário no banco
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users

@app.get("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def read_user(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Usuário não encontrado'
        )
        
    return db_user

@app.put("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def update_user(id: int, user: BaseUsuario, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Usuário não encontrado'
        )
    
    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        
        session.commit()
        session.refresh(db_user)
        return db_user
        
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nome de usuário ou Email já existe'
        )

@app.delete("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def delete_user(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Usuário não encontrado'
        )
    
    session.delete(db_user)
    session.commit()
    
    return db_user