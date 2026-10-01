# API de Gerenciamento de Corridas de Rua

Uma API RESTful moderna, assíncrona e robusta para gerenciar corridas de rua, construída com **FastAPI** e **SQLAlchemy 2.0**. Este projeto foi desenvolvido como uma evolução prática de um material acadêmico, corrigindo inconsistências e aplicando as melhores práticas atuais de desenvolvimento Python.

## Funcionalidades

- **Usuários**: Cadastro com hash de senha seguro (bcrypt), listagem e busca.
- **Corridas (Races)**: CRUD completo com validação de dados e relacionamento com organizadores.
- **Inscrições (Registrations)**: Registro de corredores em corridas com controle de status.
- **Resultados**: Registro de posições e tempos finais de conclusão.
- **Segurança**: Senhas criptografadas, validação rigorosa de schemas (Pydantic V2) e proteção contra injeção de SQL via ORM.

## Tecnologias Utilizadas

- **Python 3.10+** (Gerenciado via `pyenv`)
- **FastAPI**: Framework web moderno e de alta performance
- **SQLAlchemy 2.0**: ORM assíncrono (`asyncpg`)
- **PostgreSQL**: Banco de dados relacional (via Docker)
- **Pydantic V2**: Validação e serialização de dados
- **bcrypt**: Hashing seguro de senhas
- **Uvicorn**: Servidor ASGI

## Pré-requisitos

- Python 3.10 ou superior (recomendado: `pyenv`)
- Docker e Docker Compose
- Git

## Instalação e Configuração

### 1. Clonar o repositório e entrar na pasta
```bash
git clone <url-do-seu-repositorio>
cd uninter-apis-corrida
```

### 2. Configurar o ambiente Python
```bash
# Definir a versão do Python (ex: 3.10.19)
pyenv local 3.10.19

# Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Subir o Banco de Dados (Docker)
```bash
docker run -d \
  --name corrida-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=corrida \
  -p 5432:5432 \
  postgres:16-alpine
```

### 5. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/corrida
```

### 6. Criar as tabelas no banco
```bash
python criar_tabelas.py
```

## Executando a Aplicação

Inicie o servidor de desenvolvimento com recarregamento automático:
```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## Documentação da API

O FastAPI gera documentação automática e interativa. Após iniciar o servidor, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Exemplos de Uso (cURL)

### 1. Criar um Usuário (Organizador)
```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Marcos Organizador",
    "email": "marcos@corrida.com",
    "password": "senha_segura_123",
    "role": "organizador"
  }'
```

### 2. Criar uma Corrida
*(Use o `id` do usuário criado acima como `organizer_id`)*
```bash
curl -X POST http://localhost:8000/api/v1/races/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Corrida de São Silvestre",
    "date": "2026-12-31",
    "location": "São Paulo, SP",
    "distance": 15.0,
    "description": "Corrida tradicional de fim de ano",
    "organizer_id": 1
  }'
```

### 3. Listar todas as Corridas
```bash
curl http://localhost:8000/api/v1/races/
```

## Estrutura do Projeto

```text
.
├── api/
│   └── v1/
│       ├── api.py                 # Router principal que agrega os endpoints
│       └── endpoints/             # Rotas CRUD (user.py, race.py, etc.)
├── core/
│   ├── configs.py                 # Configurações (DB_URL, DBBaseModel)
│   └── deps.py                    # Injeção de dependência (get_session)
├── models/                        # Modelos SQLAlchemy (Mapeamento do Banco)
├── schemas/                       # Modelos Pydantic (Validação JSON)
├── criar_tabelas.py               # Script para gerar o schema no PostgreSQL
├── main.py                        # Ponto de entrada da aplicação FastAPI
├── requirements.txt               # Dependências do projeto
└── .env                           # Variáveis de ambiente (não versionado)
```

## Melhorias em relação ao material original

Este projeto foi intencionalmente refinado para evitar armadilhas comuns:
1. **SQLAlchemy 2.0**: Uso da sintaxe moderna `Mapped` e `mapped_column` (type-safe), substituindo a sintaxe legada `Column`.
2. **Correção de Conflitos de Nome**: Resolução do bug de colisão do import `time` usando `from datetime import time as TimeType`.
3. **Segurança Real**: Substituição da biblioteca `passlib` (que possui bugs de compatibilidade com versões recentes do `bcrypt`) pelo uso direto e nativo do `bcrypt`.
4. **Injeção de Dependência Correta**: Uso de `db: AsyncSession = Depends(get_session)` em vez de context managers (`async with db as session`) incorretos para objetos já injetados.
5. **Separação Rigorosa de Schemas**: Implementação de `Base`, `Create` e `Response` para evitar vazamento de dados sensíveis (como senhas) ou injeção de campos indesejados (como `id`).

## Autor

Desenvolvido com foco em aprendizado, arquitetura limpa e boas práticas de mercado.
