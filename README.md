# API de Gerenciamento de Corridas de Rua (Fullstack)

Uma aplicação fullstack moderna, assíncrona e robusta para gerenciar corridas de rua. O backend é construído com **FastAPI** e **SQLAlchemy 2.0**, enquanto o frontend utiliza **Vue.js 3** e **Vite**, comunicando-se de forma segura e eficiente.

Este projeto foi desenvolvido como uma evolução prática de um material acadêmico, aplicando as melhores práticas atuais de desenvolvimento de software, segurança e arquitetura limpa.

## Funcionalidades

- **Usuários**: Cadastro com hash de senha seguro (bcrypt), listagem e busca.
- **Corridas (Races)**: CRUD completo com validação de dados e relacionamento com organizadores.
- **Inscrições (Registrations)**: Registro de corredores em corridas com controle de status.
- **Resultados**: Registro de posições e tempos finais de conclusão.
- **Interface Web**: Dashboard reativo em Vue.js que consome a API em tempo real.
- **Segurança**: Senhas criptografadas, validação rigorosa de schemas (Pydantic V2) e proteção contra injeção de SQL via ORM.

## Tecnologias Utilizadas

**Backend:**
- **Python 3.10+** (Gerenciado via `pyenv`)
- **FastAPI**: Framework web moderno e de alta performance
- **SQLAlchemy 2.0**: ORM assíncrono (`asyncpg`) com sintaxe type-safe (`Mapped`)
- **PostgreSQL 16**: Banco de dados relacional (via Docker)
- **Pydantic V2**: Validação e serialização de dados
- **bcrypt**: Hashing seguro de senhas
- **Uvicorn**: Servidor ASGI

**Frontend:**
- **Vue.js 3**: Framework JavaScript progressivo e reativo
- **Vite**: Build tool ultrarrápida para desenvolvimento
- **Axios**: Cliente HTTP para comunicação com a API

## Pré-requisitos

- Python 3.10 ou superior (recomendado: `pyenv`)
- Node.js 20+ (recomendado: usar `nvm` para gerenciar versões)
- Docker e Docker Compose
- Git

## Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone <url-do-seu-repositorio>
cd race-management-api # ou o nome que você escolheu
```

### 2. Configurar o ambiente Python
```bash
pyenv local 3.10.19
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

### 3. Instalar dependências do Backend
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

### 7. Configurar o Frontend (Vue.js)
```bash
cd frontend
npm install
cd .. # Volta para a raiz do projeto
```

## Executando a Aplicação

Você precisará de **dois terminais** abertos na raiz do projeto:

**Terminal 1: Backend (FastAPI)**
```bash
uvicorn main:app --reload
```
*A API estará disponível em: `http://localhost:8000`*

**Terminal 2: Frontend (Vue.js)**
```bash
cd frontend
npm run dev
```
*A interface web estará disponível em: `http://localhost:5173`*

## Documentação da API

O FastAPI gera documentação automática e interativa (Swagger UI). Com o backend rodando, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Exemplos de Uso (cURL para Backend)

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

## 📂 Estrutura do Projeto

```text
.
├── api/v1/
│   ├── api.py                 # Router principal que agrega os endpoints
│   └── endpoints/             # Rotas CRUD (user.py, race.py, registration.py, result.py)
├── core/
│   ├── configs.py             # Configurações (DB_URL, DBBaseModel)
│   └── deps.py                # Injeção de dependência (get_session)
├── models/                    # Modelos SQLAlchemy 2.0 (Mapeamento do Banco)
├── schemas/                   # Modelos Pydantic V2 (Validação JSON)
├── frontend/                  # Projeto Vue.js (Vite + Axios)
│   ├── src/
│   │   ├── components/        # Componentes reutilizáveis (ex: RacesList.vue)
│   │   ├── App.vue            # Componente raiz
│   │   └── main.js            # Ponto de entrada do Vue
│   └── package.json
├── criar_tabelas.py           # Script para gerar o schema no PostgreSQL
├── main.py                    # Ponto de entrada da aplicação FastAPI (com CORS)
├── requirements.txt           # Dependências Python
└── .env                       # Variáveis de ambiente (não versionado)
```

## Melhorias e Boas Práticas Aplicadas

Este projeto foi intencionalmente refinado para ir além do básico, garantindo robustez e manutenibilidade:

1. **SQLAlchemy 2.0 Nativo**: Uso da sintaxe moderna `Mapped` e `mapped_column` (type-safe), substituindo a sintaxe legada `Column`.
2. **Segurança Real**: Substituição de bibliotecas obsoletas pelo uso direto e nativo do `bcrypt` para hash de senhas, atendendo a requisitos de segurança de dados.
3. **Injeção de Dependência Assíncrona Correta**: Uso de `db: AsyncSession = Depends(get_session)` com `yield`, garantindo o fechamento correto das conexões.
4. **Separação Rigorosa de Schemas**: Implementação de `Base`, `Create` e `Response` no Pydantic para evitar vazamento de dados sensíveis (como senhas) ou injeção de campos indesejados (como `id`).
5. **Resolução de Conflitos e CORS**: Ajuste fino de imports (ex: `time as TimeType`) e configuração precisa de middleware CORS no FastAPI, incluindo o uso de barras finais em rotas Axios para evitar redirecionamentos 307 que quebram a comunicação frontend-backend.

## Autor

Desenvolvido com foco em aprendizado contínuo, arquitetura limpa e boas práticas de mercado.
