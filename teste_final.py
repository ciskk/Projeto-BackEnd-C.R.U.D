import requests

url = 'http://127.0.0.1:8000'

def roda_o_script():
    print("iniciando os testes pro bismarck ver")

    # 1. teste de senha fraca
    print("\n1. testando se barra senha paia")
    user_paia = {
        "username": "bismarck_fake",
        "email": "prefeito@aracati.com",
        "password": "soletra" 
    }
    r = requests.post(f"{url}/usuarios", json=user_paia)
    
    if r.status_code == 400:
        print("barrou a senha, api ta segura")
    else:
        print("deu ruim, deixou passar senha fraca", r.status_code)

    # 2. criar usuario oficial
    print("\n2. criando o chico no banco")
    user_chico = {
        "username": "chico_aracati",
        "email": "francisco@dev.com",
        "password": "senhaForte123"
    }
    
    # limpa se o chico ja existir de outro teste
    try:
        busca = requests.get(f"{url}/usuarios/busca/chico_aracati")
        if busca.status_code == 200:
            id_velho = busca.json()['id']
            requests.delete(f"{url}/usuarios/{id_velho}")
    except:
        pass

    r = requests.post(f"{url}/usuarios", json=user_chico)
    
    id_chico = None
    if r.status_code == 201:
        dados = r.json()
        id_chico = dados['id']
        print("criou o chico com sucesso, id", id_chico)
    elif r.status_code == 409:
        print("o chico ja existe la")
    else:
        print("erro ao criar o chico", r.text)
        return

    # 3. buscar por id
    if id_chico:
        print("\n3. buscando id do chico")
        r = requests.get(f"{url}/usuarios/{id_chico}")
        if r.status_code == 200:
            print("achou os dados:", r.json())
        else:
            print("nao achou o id nao")

    # 4. buscar por nome
    print("\n4. buscando pelo nome de usuario")
    r = requests.get(f"{url}/usuarios/busca/chico_aracati")
    if r.status_code == 200:
        print("achou o chico pelo nome tb")
    else:
        print("nao achou pelo nome")

    # 5. atualizar
    if id_chico:
        print("\n5. atualizando email pro bismarck aprovar")
        novo_dado = {
            "username": "chico_aracati",
            "email": "chico_novo@aracati.ce.gov.br",
            "password": "senhaForte123"
        }
        r = requests.put(f"{url}/usuarios/{id_chico}", json=novo_dado)
        if r.status_code == 200:
            print("atualizou certinho:", r.json())
        else:
            print("erro ao atualizar", r.status_code)

    # 6. deletar
    if id_chico:
        print("\n6. deletando o rastro")
        r = requests.delete(f"{url}/usuarios/{id_chico}")
        if r.status_code == 200:
            print("usuario deletado, vlw")
        else:
            print("erro ao deletar")

    print("\nfim, pode entregar")

if __name__ == "__main__":
    try:
        roda_o_script()
    except:
        print("deu erro de conexao, liga o uvicorn ai")