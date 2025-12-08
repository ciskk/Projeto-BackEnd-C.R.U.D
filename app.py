from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_session
from models import User
from schema import UsuarioPublic, BaseUsuario, Usuario

app = FastAPI(title='API de Receitas e Usuarios')

#Funcao Auxiliar
def senha_eh_forte(senha: str) -> bool:
    # Verifica se tem letras E numeros
    tem_letra = any(c.isalpha() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    return tem_letra and tem_numero

#ROTAS DE USUÁRIOS

@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(user: BaseUsuario, session: Session = Depends(get_session)):
    # Valida senha
    if not senha_eh_forte(user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='A senha precisa ter letras e numeros'
        )

    # Verifica duplicados
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=409, detail='Nome de usuario ja existe')
        elif db_user.email == user.email:
            raise HTTPException(status_code=409, detail='Email ja existe')

    # Cria no banco
    novo_usuario = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario

@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def get_todos_usuarios(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users

@app.get("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def get_usuario_por_id(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    
    if not db_user:
        raise HTTPException(status_code=404, detail='Usuario nao encontrado')
        
    return db_user

@app.get("/usuarios/busca/{nome}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def get_usuario_por_nome(nome: str, session: Session = Depends(get_session)):
    # Busca exata pelo username
    db_user = session.scalar(select(User).where(User.username == nome))
    
    if not db_user:
        raise HTTPException(status_code=404, detail='Usuario nao encontrado')
    
    return db_user

@app.put("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def update_usuario(id: int, user: BaseUsuario, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    
    if not db_user:
        raise HTTPException(status_code=404, detail='Usuario nao encontrado')
    
    # Valida senha na atualizacao tambem
    if not senha_eh_forte(user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='A senha precisa ter letras e numeros'
        )

    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        
        session.commit()
        session.refresh(db_user)
        return db_user
        
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail='Nome ou Email ja existe')

@app.delete("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def delete_usuario(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    
    if not db_user:
        raise HTTPException(status_code=404, detail='Usuario nao encontrado')
    
    session.delete(db_user)
    session.commit()
    
    return db_user