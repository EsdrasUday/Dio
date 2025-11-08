# Desafio - API Assíncrona com FastAPI (DIO)

Este projeto é o desafio proposto no módulo **"APIs Assíncronas com FastAPI"** da trilha Python da [Digital Innovation One (DIO)](https://www.dio.me/).

O objetivo é desenvolver uma API RESTful assíncrona para gerenciar contas de um sistema financeiro simples, aplicando os conceitos de FastAPI, SQLAlchemy Core, `databases` para acesso assíncrono ao banco de dados e Pydantic para validação de esquemas.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI:** Framework web moderno e assíncrono.
* **SQLAlchemy Core:** Para construção de queries SQL de forma programática.
* **Databases:** Biblioteca para fornecer conectividade assíncrona ao banco de dados (SQLite, PostgreSQL, etc.).
* **Pydantic:** Para validação de dados e definição de esquemas (schemas).
* **Uvicorn:** Servidor ASGI para rodar a aplicação FastAPI.

---

## 📂 Estrutura do Projeto

O projeto segue uma estrutura modular para separar responsabilidades:

```
/desafio
├── src/
│   ├── __init__.py
│   ├── main.py         # Ponto de entrada da API, define os endpoints
│   ├── database.py     # Configuração da conexão com o BD (objeto 'database')
│   ├── models/
│   │   ├── __init__.py
│   │   └── account.py  # Modelo da tabela 'accounts' (SQLAlchemy)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── account.py  # Schemas Pydantic (AccountIn, AccountOut)
│   └── services/
│       ├── __init__.py
│       └── account.py  # Lógica de negócio (AccountService)
└── requirements.txt    # Lista de dependências do projeto
```

---

## 🚀 Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Clonar o Repositório

```bash
# Clone este fork ou o repositório original
git clone [https://github.com/digitalinnovationone/trilha-python-dio.git](https://github.com/digitalinnovationone/trilha-python-dio.git)

# Navegue até o diretório do desafio
cd "trilha-python-dio/13 - APIs Assíncronas com FastAPI/desafio"
```

### 2. Criar e Ativar um Ambiente Virtual

É uma boa prática usar um ambiente virtual para gerenciar as dependências.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente (Linux/macOS)
source venv/bin/activate

# Ativar o ambiente (Windows)
.\venv\Scripts\activate
```

### 3. Instalar as Dependências

As dependências principais estão listadas abaixo. Crie um arquivo `requirements.txt` com este conteúdo e instale-o.

**`requirements.txt`**

```
fastapi
uvicorn[standard]
sqlalchemy
databases[sqlite]
pydantic
```

**Comando de instalação:**

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação

Este projeto usa o **Uvicorn** como servidor ASGI.

```bash
# O Uvicorn irá iniciar o servidor e recarregar automaticamente após mudanças
uvicorn src.main:app --reload
```

Após executar o comando, a API estará disponível em `http://127.0.0.1:8000`.

---

## 📖 Endpoints da API

A API fornece os seguintes endpoints para gerenciamento de contas:

### 1. Criar uma Conta

Cria uma nova conta no sistema.

* **Endpoint:** `POST /accounts`
* **Request Body (`AccountIn`):**
    ```json
    {
      "user_id": 1,
      "balance": 150.75
    }
    ```
* **Response (200 OK):** Retorna a conta recém-criada, incluindo `id` e `created_at`.
    ```json
    {
      "id": 1,
      "user_id": 1,
      "balance": "150.75",
      "created_at": "2025-11-08T15:00:00.000000+00:00"
    }
    ```

### 2. Listar Contas (com Paginação)

Retorna uma lista de todas as contas, com suporte para paginação usando `skip` e `limit`.

* **Endpoint:** `GET /accounts`
* **Query Parameters:**
    * `limit: int` (Obrigatório) - Número máximo de registros a retornar.
    * `skip: int` (Opcional, `default = 0`) - Número de registros a pular (offset).
* **Exemplo de Requisição:** `GET http://127.0.0.1:8000/accounts?limit=10&skip=0`
* **Response (200 OK):** Uma lista de objetos de conta.
    ```json
    [
      {
        "id": 1,
        "user_id": 1,
        "balance": "150.75",
        "created_at": "2025-11-08T15:00:00.000000+00:00"
      },
      {
        "id": 2,
        "user_id": 2,
        "balance": "500.00",
        "created_at": "2025-11-08T15:01:00.000000+00:00"
      }
    ]
    ```
