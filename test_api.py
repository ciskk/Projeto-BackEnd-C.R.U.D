import requests
import json

BASE_URL = 'http://localhost:5000'

def test_create_recipe():
    """Testa a criação de uma receita"""
    recipe_data = {
        'nome': 'Bolo de Chocolate',
        'ingredientes': ['farinha', 'açúcar', 'chocolate', 'ovos', 'leite'],
        'modo_de_preparo': 'Misture todos os ingredientes e asse por 30 minutos'
    }
    
    response = requests.post(f'{BASE_URL}/recipes', json=recipe_data)
    print(f"POST /recipes - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    return response.json()

def test_get_all_recipes():
    """Testa a listagem de todas as receitas"""
    response = requests.get(f'{BASE_URL}/recipes')
    print(f"GET /recipes - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_get_recipe_by_id(recipe_id):
    """Testa a busca de receita por ID"""
    response = requests.get(f'{BASE_URL}/recipes/{recipe_id}')
    print(f"GET /recipes/{recipe_id} - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_update_recipe(recipe_id):
    """Testa a atualização de uma receita"""
    update_data = {
        'nome': 'Bolo de Chocolate Especial',
        'ingredientes': ['farinha', 'açúcar', 'chocolate amargo', 'ovos', 'leite', 'manteiga'],
        'modo_de_preparo': 'Misture todos os ingredientes, adicione a manteiga e asse por 35 minutos'
    }
    
    response = requests.put(f'{BASE_URL}/recipes/{recipe_id}', json=update_data)
    print(f"PUT /recipes/{recipe_id} - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_delete_recipe(recipe_id):
    """Testa a exclusão de uma receita"""
    response = requests.delete(f'{BASE_URL}/recipes/{recipe_id}')
    print(f"DELETE /recipes/{recipe_id} - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_validation_errors():
    """Testa os casos de erro de validação"""
    print("=== TESTANDO VALIDAÇÕES ===")
    
    # Nome muito curto
    invalid_recipe = {
        'nome': 'A',
        'ingredientes': ['farinha'],
        'modo_de_preparo': 'Teste'
    }
    response = requests.post(f'{BASE_URL}/recipes', json=invalid_recipe)
    print(f"Nome muito curto - Status: {response.status_code}, Response: {response.json()}")
    
    # Nome muito longo
    invalid_recipe = {
        'nome': 'A' * 51,
        'ingredientes': ['farinha'],
        'modo_de_preparo': 'Teste'
    }
    response = requests.post(f'{BASE_URL}/recipes', json=invalid_recipe)
    print(f"Nome muito longo - Status: {response.status_code}, Response: {response.json()}")
    
    # Muitos ingredientes
    invalid_recipe = {
        'nome': 'Receita Teste',
        'ingredientes': ['ingrediente'] * 21,
        'modo_de_preparo': 'Teste'
    }
    response = requests.post(f'{BASE_URL}/recipes', json=invalid_recipe)
    print(f"Muitos ingredientes - Status: {response.status_code}, Response: {response.json()}")
    print("-" * 50)

if __name__ == '__main__':
    print("=== INICIANDO TESTES DA API ===")
    
    # Criar uma receita
    created_recipe = test_create_recipe()
    recipe_id = created_recipe.get('id')
    
    # Listar todas as receitas
    test_get_all_recipes()
    
    # Buscar receita por ID
    if recipe_id:
        test_get_recipe_by_id(recipe_id)
        
        # Atualizar receita
        test_update_recipe(recipe_id)
        
        # Listar novamente para ver a atualização
        test_get_all_recipes()
        
        # Deletar receita
        test_delete_recipe(recipe_id)
        
        # Listar novamente para confirmar exclusão
        test_get_all_recipes()
    
    # Testar validações
    test_validation_errors()
    
    print("=== TESTES CONCLUÍDOS ===")
