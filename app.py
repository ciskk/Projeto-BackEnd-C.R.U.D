from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from http import HTTPStatus # Importa HTTPStatus conforme o PDF

app = FastAPI()

# --- Modelos de Receita (Existentes) ---
class RecipeCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50)
    ingredientes: List[str] = Field(..., min_items=1, max_items=20)
    modo_de_preparo: str

class RecipeUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=50)
    ingredientes: Optional[List[str]] = Field(None, min_items=1, max_items=20)
    modo_de_preparo: Optional[str] = None

class RecipeInDB(RecipeCreate):
    id: int

# --- Modelos de Usuário (Novos) ---
class BaseUsuario(BaseModel):
    nome_usuario: str = Field(..., min_length=3, max_length=50)
    email: str
    senha: str = Field(..., min_length=4) # Mínimo de 4 para o desafio

class Usuario(BaseUsuario):
    id: int

class UsuarioPublic(BaseModel):
    id: int
    nome_usuario: str
    email: str

# --- Banco de Dados em Memória ---
recipes_db: List[RecipeInDB] = []
recipe_id_counter = 1

usuarios_db: List[Usuario] = [] # Novo banco de dados para usuários
user_id_counter = 1 # Novo contador para IDs de usuário

# --- Helper: Validação de Senha (Desafio Extra) ---
def is_senha_valida(senha: str) -> bool:
    """Verifica se a senha contém pelo menos uma letra e um número."""
    tem_letra = any(c.isalpha() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    return tem_letra and tem_numero

# --- Rotas de Receitas (Existentes - Status Code Atualizado) ---

# Atualizei os status_code para usar HTTPStatus, como no PDF
@app.post("/recipes/", response_model=RecipeInDB, status_code=HTTPStatus.CREATED)
async def create_recipe(recipe: RecipeCreate):
    global recipe_id_counter

    if any(r.nome.lower() == recipe.nome.lower() for r in recipes_db):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Já existe uma receita com este nome")

    new_recipe = RecipeInDB(id=recipe_id_counter, **recipe.dict())
    recipes_db.append(new_recipe)
    recipe_id_counter += 1
    return new_recipe

@app.get("/recipes/", response_model=List[RecipeInDB], status_code=HTTPStatus.OK)
async def get_all_recipes():
    return recipes_db

@app.get("/recipes/{recipe_id}", response_model=RecipeInDB, status_code=HTTPStatus.OK)
async def get_recipe_by_id(recipe_id: int):
    recipe = next((r for r in recipes_db if r.id == recipe_id), None)
    if recipe:
        return recipe
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.put("/recipes/{recipe_id}", response_model=RecipeInDB, status_code=HTTPStatus.OK)
async def update_recipe(recipe_id: int, recipe_update: RecipeUpdate):
    recipe_index = next((i for i, r in enumerate(recipes_db) if r.id == recipe_id), None)

    if recipe_index is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

    current_recipe = recipes_db[recipe_index]
    update_data = recipe_update.dict(exclude_unset=True)

    if "nome" in update_data:
        if update_data["nome"].strip() == "":
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita não pode ser vazio")
        if any(r.nome.lower() == update_data["nome"].lower() and r.id != recipe_id for r in recipes_db):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Já existe outra receita com este nome")

    for key, value in update_data.items():
        setattr(current_recipe, key, value)

    return current_recipe

@app.delete("/recipes/{recipe_id}", status_code=HTTPStatus.OK)
async def delete_recipe(recipe_id: int):
    global recipes_db
    if not recipes_db:
        # Mantendo sua lógica original, embora GET /recipes já cobriria isso
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A lista de receitas está vazia")

    recipe_index = next((i for i, r in enumerate(recipes_db) if r.id == recipe_id), None)

    if recipe_index is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

    deleted_recipe = recipes_db.pop(recipe_index)
    return {"message": "Receita deletada", "recipe": deleted_recipe}

# --- ROTAS DE USUÁRIO (Novas) ---

@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
async def create_usuario(dados: BaseUsuario):
    """
    Cria um novo usuário.
    - Valida se o email já existe.
    - Valida se a senha atende aos critérios (letras e números).
    """
    global user_id_counter
    
    # 3. Validação de email duplicado
    if any(u.email.lower() == dados.email.lower() for u in usuarios_db):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email já cadastrado."
        )
    
    # Desafio Extra: Validação de senha
    if not is_senha_valida(dados.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter pelo menos uma letra e um número."
        )

    # 2. Lógica de criação (seguindo seu padrão)
    novo_usuario = Usuario(id=user_id_counter, **dados.dict())
    usuarios_db.append(novo_usuario)
    user_id_counter += 1
    # FastAPI cuidará de converter Usuario -> UsuarioPublic no retorno
    return novo_usuario

@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
async def get_todos_usuarios():
    """Retorna todos os usuários cadastrados."""
    return usuarios_db

@app.get("/usuarios/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
async def get_usuario_por_nome(nome_usuario: str):
    """Busca um usuário específico pelo seu nome_usuario."""
    usuario = next((u for u in usuarios_db if u.nome_usuario.lower() == nome_usuario.lower()), None)
    if usuario:
        return usuario
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Usuário não encontrado."
    )

@app.get("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
async def get_usuario_por_id(id: int):
    """Busca um usuário específico pelo seu ID."""
    usuario = next((u for u in usuarios_db if u.id == id), None)
    if usuario:
        return usuario
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Usuário não encontrado."
    )

@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
async def update_usuario(id: int, dados: BaseUsuario):
    """
    Atualiza um usuário existente.
    - Valida a senha.
    - Valida se o novo email já está em uso por outro usuário.
    """
    usuario_index = next((i for i, u in enumerate(usuarios_db) if u.id == id), None)

    if usuario_index is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    # Desafio Extra: Validação de senha
    if not is_senha_valida(dados.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter pelo menos uma letra e um número."
        )
    
    # Validação de email duplicado (exceto ele mesmo)
    if any(u.email.lower() == dados.email.lower() and u.id != id for u in usuarios_db):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email já cadastrado por outro usuário."
        )

    usuario_atualizado = Usuario(id=id, **dados.dict())
    usuarios_db[usuario_index] = usuario_atualizado
    return usuario_atualizado

@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
async def delete_usuario(id: int):
    """Deleta um usuário pelo ID e retorna o usuário deletado."""
    usuario_index = next((i for i, u in enumerate(usuarios_db) if u.id == id), None)

    if usuario_index is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )

    deleted_usuario = usuarios_db.pop(usuario_index)
    # Retorna o usuário deletado (como UsuarioPublic) conforme o PDF
    return deleted_usuario

