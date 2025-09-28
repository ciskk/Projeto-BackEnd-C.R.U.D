
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

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

recipes_db: List[RecipeInDB] = []
recipe_id_counter = 1

@app.post("/recipes/", response_model=RecipeInDB, status_code=201)
async def create_recipe(recipe: RecipeCreate):
    global recipe_id_counter

    if any(r.nome.lower() == recipe.nome.lower() for r in recipes_db):
        raise HTTPException(status_code=400, detail="Já existe uma receita com este nome")

    new_recipe = RecipeInDB(id=recipe_id_counter, **recipe.dict())
    recipes_db.append(new_recipe)
    recipe_id_counter += 1
    return new_recipe

@app.get("/recipes/", response_model=List[RecipeInDB])
async def get_all_recipes():
    return recipes_db

@app.get("/recipes/{recipe_id}", response_model=RecipeInDB)
async def get_recipe_by_id(recipe_id: int):
    recipe = next((r for r in recipes_db if r.id == recipe_id), None)
    if recipe:
        return recipe
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.put("/recipes/{recipe_id}", response_model=RecipeInDB)
async def update_recipe(recipe_id: int, recipe_update: RecipeUpdate):
    recipe_index = next((i for i, r in enumerate(recipes_db) if r.id == recipe_id), None)

    if recipe_index is None:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    current_recipe = recipes_db[recipe_index]
    update_data = recipe_update.dict(exclude_unset=True)

    if "nome" in update_data:
        if update_data["nome"].strip() == "":
            raise HTTPException(status_code=400, detail="O nome da receita não pode ser vazio")
        if any(r.nome.lower() == update_data["nome"].lower() and r.id != recipe_id for r in recipes_db):
            raise HTTPException(status_code=400, detail="Já existe outra receita com este nome")

    for key, value in update_data.items():
        setattr(current_recipe, key, value)

    return current_recipe

@app.delete("/recipes/{recipe_id}", status_code=200)
async def delete_recipe(recipe_id: int):
    global recipes_db
    if not recipes_db:
        raise HTTPException(status_code=400, detail="A lista de receitas está vazia")

    recipe_index = next((i for i, r in enumerate(recipes_db) if r.id == recipe_id), None)

    if recipe_index is None:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    deleted_recipe = recipes_db.pop(recipe_index)
    return {"message": "Receita deletada", "recipe": deleted_recipe}

