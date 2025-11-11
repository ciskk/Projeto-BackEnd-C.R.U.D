import requests
import json

BASE_URL = 'http://127.0.0.1:8000'


def test_create_recipe():
    """Testa a criação de uma receita"""
    recipe_data = {
        'nome': 'Bolo de Chocolate',
        'ingredientes': ['farinha', 'açúcar', 'chocolate', 'ovos', 'leite'],
        'modo_de_preparo': 'Misture todos os ingredientes e asse por 30 minutos'
    }
    
    response = requests.post(f'{BASE_URL}/recipes/', json=recipe_data)
    print(f"POST /recipes/ - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    return response.json()

def test_get_all_recipes():
    """Testa a listagem de todas as receitas"""
    response = requests.get(f'{BASE_URL}/recipes/')
    print(f"GET /recipes/ - Status: {response.status_code}")
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
    print("=== TESTANDO VALIDAÇÕES DE RECEITAS ===")
    
    # Nome muito curto
    invalid_recipe = {
        'nome': 'A',
        'ingredientes': ['farinha'],
        'modo_de_preparo': 'Teste'
    }
    response = requests.post(f'{BASE_URL}/recipes/', json=invalid_recipe)
    print(f"Nome muito curto - Status: {response.status_code}, Response: {response.json()}")
    
    # Nome muito longo
    invalid_recipe = {
        'nome': 'A' * 51,
        'ingredientes': ['farinha'],
        'modo_de_preparo': 'Teste'
    }
    response = requests.post(f'{BASE_URL}/recipes/', json=invalid_recipe)
    print(f"Nome muito longo - Status: {response.status_code}, Response: {response.json()}")
    
    # Muitos ingredientes
    invalid_recipe = {
        'nome': 'Receita Teste',
        'ingredientes': ['ingrediente'] * 21,
        'modo_de_preparo': 'Teste'
    }
    response = requests.post(f'{BASE_URL}/recipes/', json=invalid_recipe)
    print(f"Muitos ingredientes - Status: {response.status_code}, Response: {response.json()}")
    
    # Nome vazio na atualização
    update_empty_name = {
        'nome': ''
    }
    response = requests.put(f'{BASE_URL}/recipes/1', json=update_empty_name)
    print(f"Nome vazio na atualização - Status: {response.status_code}, Response: {response.json()}")
    print("-" * 50)

# --- TESTES DE USUÁRIOS (Novos) ---

def test_create_usuario():
    """Testa a criação de um usuário válido"""
    user_data = {
        'nome_usuario': 'ana_dev',
        'email': 'ana@dev.com',
        'senha': 'senhaCom1Numero'
    }
    response = requests.post(f'{BASE_URL}/usuarios', json=user_data)
    print(f"POST /usuarios - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    assert response.status_code == 201
    assert response.json()['email'] == 'ana@dev.com'
    assert 'senha' not in response.json() # Confirma que é UsuarioPublic
    return response.json()

def test_create_usuario_email_duplicado():
    """Testa criar usuário com email que já existe"""
    user_data = {
        'nome_usuario': 'ana_duplicada',
        'email': 'ana@dev.com', # Email do teste anterior
        'senha': 'outraSenha123'
    }
    response = requests.post(f'{BASE_URL}/usuarios', json=user_data)
    print(f"POST /usuarios (Email duplicado) - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    assert response.status_code == 400

def test_create_usuario_senha_invalida():
    """Testa criar usuário com senha inválida (sem número)"""
    user_data = {
        'nome_usuario': 'bruno_dev',
        'email': 'bruno@dev.com',
        'senha': 'senhasemnumero'
    }
    response = requests.post(f'{BASE_URL}/usuarios', json=user_data)
    print(f"POST /usuarios (Senha inválida/sem número) - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    assert response.status_code == 400
    
    user_data['senha'] = 'semletra12345'
    response = requests.post(f'{BASE_URL}/usuarios', json=user_data)
    print(f"POST /usuarios (Senha inválida/sem letra) - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    assert response.status_code == 400

def test_get_todos_usuarios():
    """Testa a listagem de todos os usuários"""
    response = requests.get(f'{BASE_URL}/usuarios/')
    print(f"GET /usuarios/ - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_get_usuario_por_id(user_id):
    """Testa a busca de usuário por ID"""
    response = requests.get(f'{BASE_URL}/usuarios/id/{user_id}')
    print(f"GET /usuarios/id/{user_id} - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_get_usuario_por_nome(nome_usuario):
    """Testa a busca de usuário por nome_usuario"""
    response = requests.get(f'{BASE_URL}/usuarios/{nome_usuario}')
    print(f"GET /usuarios/{nome_usuario} - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_update_usuario(user_id):
    """Testa a atualização de um usuário"""
    update_data = {
        'nome_usuario': 'ana_dev_atualizada',
        'email': 'ana_nova@dev.com',
        'senha': 'novaSenha123'
    }
    response = requests.put(f'{BASE_URL}/usuarios/{user_id}', json=update_data)
    print(f"PUT /usuarios/{user_id} - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    assert response.status_code == 200
    assert response.json()['email'] == 'ana_nova@dev.com'

def test_update_usuario_senha_invalida(user_id):
    """Testa a atualização de um usuário com senha inválida"""
    update_data = {
        'nome_usuario': 'ana_dev_atualizada_fail',
        'email': 'ana_nova_fail@dev.com',
        'senha': 'senhasemnumero'
    }
    response = requests.put(f'{BASE_URL}/usuarios/{user_id}', json=update_data)
    print(f"PUT /usuarios/{user_id} (Senha inválida) - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    assert response.status_code == 400

def test_delete_usuario(user_id):
    """Testa a exclusão de um usuário"""
    response = requests.delete(f'{BASE_URL}/usuarios/{user_id}')
    print(f"DELETE /usuarios/{user_id} - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    assert response.status_code == 200

# Bloco Principal de Execução de Testes 

if __name__ == '__main__':
    print("=== INICIANDO TESTES DA API (RECEITAS) ===")
    
    # Criar uma receita
    created_recipe = test_create_recipe()
    recipe_id = created_recipe.get('id')
    
    # Listar todas as receitas
    test_get_all_recipes()
    
    # Testar GET, PUT, DELETE da receita criada
    if recipe_id:
        test_get_recipe_by_id(recipe_id)
        test_update_recipe(recipe_id)
        test_get_all_recipes() # Listar novamente para ver a atualização
        test_delete_recipe(recipe_id)
        test_get_all_recipes() # Listar novamente para confirmar exclusão
    
    # Testar validações de receita
    test_validation_errors()
    
    print("\n" + "=" * 20)
    print("=== INICIANDO TESTES DA API (USUÁRIOS) ===")
    print("=" * 20 + "\n")
    
    # Criar um usuário
    created_user = test_create_usuario()
    user_id = created_user.get('id')
    user_nome = created_user.get('nome_usuario')
    
    # Testar validações de usuário
    test_create_usuario_email_duplicado()
    test_create_usuario_senha_invalida()
    
    # Listar todos os usuários
    test_get_todos_usuarios()
    
    # Testar GET, PUT, DELETE do usuário criado
    if user_id:
        test_get_usuario_por_id(user_id)
        test_get_usuario_por_nome(user_nome)
        test_update_usuario(user_id)
        test_update_usuario_senha_invalida(user_id) # Testar falha de update
        test_get_all_recipes() # Listar novamente para ver a atualização
        test_delete_usuario(user_id)
        test_get_todos_usuarios() # Listar novamente para confirmar exclusão
    
    print("\n=== TESTES CONCLUÍDOS ===")
