# API de Livro de Receitas - CRUD

Este projeto implementa uma API RESTful para gerenciamento de receitas culinárias, desenvolvida como parte da Avaliação N3 da disciplina de Back End.

## 📋 Funcionalidades

A API implementa as operações CRUD (Create, Read, Update, Delete) para receitas:

- **CREATE**: Criar novas receitas
- **READ**: Listar todas as receitas ou buscar por ID
- **UPDATE**: Atualizar receitas existentes
- **DELETE**: Excluir receitas

## 🚀 Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI**: Framework web moderno e rápido para construir APIs com Python
- **Uvicorn**: Servidor ASGI para rodar aplicações FastAPI
- **Pydantic**: Para validação de dados e serialização

## 📦 Estrutura do Projeto

```
backend_crud_api/
├── app.py              # Aplicação principal da API
├── test_api.py         # Script de testes da API
├── requirements.txt    # Dependências do projeto
└── README.md          # Documentação do projeto
```

## 🔧 Instalação e Execução

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes do Python)

### Passos para execução

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd Projeto-BackEnd-C.R.U.D
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**:
   ```bash
   uvicorn app:app --reload
   ```

4. **A API estará disponível em**: `http://127.0.0.1:8000`

   Você pode acessar a documentação interativa da API (Swagger UI) em `http://127.0.0.1:8000/docs`.

## 📚 Documentação da API

### Modelo de Dados

Cada receita possui os seguintes campos:

```json
{
  "id": 1,
  "nome": "Nome da Receita",
  "ingredientes": ["ingrediente1", "ingrediente2"],
  "modo_de_preparo": "Descrição do modo de preparo"
}
```

### Endpoints

#### 1. Criar Receita
- **Método**: `POST`
- **URL**: `/recipes/`
- **Body**:
  ```json
  {
    "nome": "Bolo de Chocolate",
    "ingredientes": ["farinha", "açúcar", "chocolate", "ovos"],
    "modo_de_preparo": "Misture tudo e asse por 30 minutos"
  }
  ```
- **Resposta de Sucesso**: `201 Created`
- **Validações**:
  - Nome deve ter entre 2 e 50 caracteres
  - Deve ter entre 1 e 20 ingredientes
  - Nome não pode ser duplicado (case-insensitive)

#### 2. Listar Todas as Receitas
- **Método**: `GET`
- **URL**: `/recipes/`
- **Resposta**: Array com todas as receitas

#### 3. Buscar Receita por ID
- **Método**: `GET`
- **URL**: `/recipes/{recipe_id}`
- **Resposta**: Dados da receita específica

#### 4. Atualizar Receita
- **Método**: `PUT`
- **URL**: `/recipes/{recipe_id}`
- **Body**: Campos que deseja atualizar
- **Validações**:
  - Nome deve ter entre 2 e 50 caracteres (se fornecido)
  - Deve ter entre 1 e 20 ingredientes (se fornecido)
  - Nome não pode ser duplicado (case-insensitive)
  - Nome não pode ser vazio

#### 5. Deletar Receita
- **Método**: `DELETE`
- **URL**: `/recipes/{recipe_id}`
- **Resposta**: Confirmação da exclusão com dados da receita deletada

## 🧪 Testando a API

O projeto inclui um script de testes (`test_api.py`) que valida todas as funcionalidades:

```bash
python test_api.py
```

### Testes Manuais com curl

#### Criar uma receita:
```bash
curl -X POST http://127.0.0.1:8000/recipes/ \
  -H "Content-Type: application/json" \
  -d 
  '{
    "nome": "Brigadeiro",
    "ingredientes": ["leite condensado", "chocolate em pó", "manteiga"],
    "modo_de_preparo": "Misture tudo e cozinhe até engrossar"
  }'
```

#### Listar receitas:
```bash
curl http://127.0.0.1:8000/recipes/
```

#### Buscar por ID:
```bash
curl http://127.0.0.1:8000/recipes/1
```

#### Atualizar receita:
```bash
curl -X PUT http://127.0.0.1:8000/recipes/1 \
  -H "Content-Type: application/json" \
  -d 
  '{
    "nome": "Brigadeiro Gourmet",
    "ingredientes": ["leite condensado", "chocolate belga", "manteiga", "granulado"]
  }'
```

#### Deletar receita:
```bash
curl -X DELETE http://127.0.0.1:8000/recipes/1
```

## ✅ Requisitos Implementados

### Funcionalidades Básicas (4,0 pts)
- ✅ **CREATE (1,0 pt)**: Criação de receitas com validação de nome duplicado
- ✅ **READ (1,0 pt)**: Listagem completa e busca por ID
- ✅ **UPDATE (1,0 pt)**: Atualização com validações de nome duplicado e vazio
- ✅ **DELETE (1,0 pt)**: Exclusão com verificações de existência

### Desafios Extra (1,0 pt)
- ✅ **Validação de nome**: Entre 2 e 50 caracteres (CREATE e UPDATE)
- ✅ **Validação de ingredientes**: Entre 1 e 20 itens (CREATE e UPDATE)
- ✅ **Comparação case-insensitive**: Para verificação de nomes duplicados

## 🔍 Regras de Negócio

1. **IDs únicos**: Cada receita recebe um ID único e incremental
2. **Nomes únicos**: Não é possível ter duas receitas com o mesmo nome (ignorando maiúsculas/minúsculas)
3. **Validações de entrada**:
   - Nome: 2-50 caracteres
   - Ingredientes: 1-20 itens
   - Modo de preparo: obrigatório
4. **Armazenamento temporário**: Dados mantidos em memória (lista Python)
5. **Tratamento de erros**: Mensagens descritivas para todos os casos de erro

## 👨‍💻 Autor
Francisco Cândido Pereira Pontes.

Projeto desenvolvido para a disciplina de Back End - Curso Técnico Integrado em Informática.

## 📄 Licença

Este projeto é desenvolvido para fins educacionais.
