# Documentação Técnica: API de Gerenciamento de Corridas de Rua

## 1. Visão Geral
Esta API RESTful foi projetada para gerenciar o ciclo de vida de corridas de rua, desde o cadastro de organizadores e corredores até a inscrição e registro de resultados. O projeto prioriza **segurança, tipagem estática e desempenho assíncrono**, utilizando as versões mais modernas e estáveis das bibliotecas do ecossistema Python.

### Stack Tecnológica
- **Linguagem**: Python 3.10+ (gerenciado via `pyenv`)
- **Framework Web**: FastAPI (alta performance, documentação automática via OpenAPI)
- **ORM**: SQLAlchemy 2.0 (sintaxe moderna com `Mapped` e `mapped_column`)
- **Banco de Dados**: PostgreSQL 16 (via Docker, driver `asyncpg`)
- **Validação**: Pydantic V2 (serialização e validação de dados)
- **Segurança**: `bcrypt` (hashing de senhas)

---

## 2. Arquitetura do Sistema
O projeto segue o padrão de **Separação de Responsabilidades**, dividindo o código em 4 camadas principais:

1. **`core/` (Infraestrutura)**: 
   - `configs.py`: Centraliza variáveis de ambiente (ex: `DB_URL`) e define a classe base `DBBaseModel` do SQLAlchemy.
   - `deps.py`: Gerencia a injeção de dependência (`get_session`), garantindo que cada requisição tenha sua própria sessão de banco de dados, que é aberta e fechada automaticamente.
2. **`models/` (Camada de Dados)**: 
   - Define como os dados são estruturados e persistidos no banco de dados (tabelas, colunas, tipos, chaves estrangeiras e ENUMs).
3. **`schemas/` (Camada de Contrato)**: 
   - Define como os dados entram e saem da API (formato JSON). Utiliza herança (`Base`, `Create`, `Response`) para reutilizar código e garantir que campos sensíveis (como senhas) nunca sejam expostos.
4. **`api/v1/endpoints/` (Camada de Rotas)**: 
   - Contém a lógica de negócio e as rotas HTTP (GET, POST, PUT, DELETE). Orquestra a comunicação entre os Schemas (entrada/saída) e os Models (banco de dados).

---

## 3. Modelagem de Dados
O banco de dados é composto por 4 entidades principais, normalizadas para evitar redundância e garantir integridade referencial:

- **`users`**: Armazena corredores e organizadores. Possui um campo `role` (ENUM) para diferenciar os tipos de acesso.
- **`races`**: Armazena os eventos. Possui uma chave estrangeira `organizer_id` vinculada à tabela `users`, garantindo que toda corrida tenha um responsável.
- **`registrations`**: Tabela de junção (N:N) que vincula um `user_id` a um `race_id`, com controle de `status` (inscrito/cancelado) e tempo estimado.
- **`results`**: Armazena o desempenho final (`position`, `finish_time`) de um usuário em uma corrida específica.

---

## 4. Fluxo de Dados (Exemplo Prático: Criar uma Corrida)
Entender como uma requisição atravessa as camadas é fundamental para dominar a arquitetura:

1. **Requisição HTTP**: O cliente envia um `POST /api/v1/races/` com um payload JSON.
2. **Validação (Schema)**: O FastAPI intercepta o JSON e o valida contra o `RaceCreate` (Pydantic). Se faltar um campo obrigatório (ex: `date`), a API rejeita a requisição com `422 Unprocessable Entity` antes mesmo de tocar no banco.
3. **Injeção de Dependência**: O FastAPI chama `get_session()` e injeta uma `AsyncSession` do SQLAlchemy no parâmetro `db` do endpoint.
4. **Lógica de Negócio (Endpoint)**: O endpoint cria uma instância do Model `Race` usando os dados validados do Schema.
5. **Persistência (Model)**: `db.add(new_race)` marca o objeto para inserção. `await db.commit()` envia o comando SQL `INSERT` para o PostgreSQL.
6. **Serialização (Schema)**: `await db.refresh(new_race)` busca os dados recém-criados (incluindo o `id` gerado pelo banco). O FastAPI converte esse objeto Model em um JSON de resposta usando o `RaceResponse`, garantindo que apenas os campos permitidos sejam retornados.

---

## 5. Decisões de Design e Boas Práticas Adotadas

| Decisão | Benefício |
| :--- | :--- |
| **SQLAlchemy 2.0 (`Mapped`)** | Substitui a sintaxe legada `Column()`. Oferece verificação de tipos nativa (type hints), melhorando o autocompletar das IDEs e prevenindo erros em tempo de desenvolvimento. |
| **Separação Rigorosa de Schemas** | Usar `UserCreate` (entrada) e `UserResponse` (saída) impede que um cliente mal-intencionado tente injetar um `id` ou `role` no cadastro, e garante que o `password` nunca vaze na resposta da API. |
| **Hashing com `bcrypt` nativo** | Garante que as senhas sejam armazenadas de forma irreversível e segura, atendendo a requisitos não funcionais de segurança e conformidade (LGPD/GDPR). |
| **Injeção de Dependência Assíncrona** | O uso de `Depends(get_session)` com `yield` garante que a conexão com o banco seja fechada corretamente ao final de cada requisição, evitando vazamento de memória e conexões órfãs. |
| **Resolução de Conflitos de Nome** | Uso de aliases (ex: `from datetime import time as TimeType`) para evitar colisões entre nomes de módulos Python e nomes de atributos das classes. |

---

## 6. Guia de Operação e Testes

### Inicialização do Ambiente
```bash
# 1. Ativar ambiente virtual
source .venv/bin/activate

# 2. Garantir que o Docker está rodando
docker start corrida-postgres

# 3. Iniciar o servidor (com recarregamento automático)
uvicorn main:app --reload
```

### Exemplos de Teste via cURL

**1. Criar um Usuário (Organizador)**
```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Marcos Organizador",
    "email": "marcos@corrida.com",
    "password": "senha_segura_123",
    "role": "organizador"
  }'
# Resposta esperada: JSON com "id": 1 e sem o campo "password".
```

**2. Criar uma Corrida**
```bash
curl -X POST http://localhost:8000/api/v1/races/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Corrida de São Silvestre",
    "date": "2026-12-31",
    "location": "São Paulo, SP",
    "distance": 15.0,
    "description": "Corrida tradicional",
    "organizer_id": 1
  }'
# Resposta esperada: JSON com "id": 1 e todos os dados da corrida.
```

**3. Consultar Documentação Interativa**
Acesse no navegador:
- **Swagger UI**: `http://localhost:8000/docs` (Permite testar os endpoints diretamente pela interface).
- **ReDoc**: `http://localhost:8000/redoc` (Documentação estática e limpa).

---

## 7. Integração Frontend (Vue.js)
O projeto evoluiu para uma arquitetura Fullstack, onde o frontend é responsável pela interface do usuário e se comunica com o backend via HTTP.

- **Framework**: Vue.js 3 (Composition/Options API) com Vite como build tool.
- **Comunicação**: Biblioteca `axios` para realizar requisições assíncronas à API.
- **Componentização**: A lógica de exibição é encapsulada em componentes reutilizáveis (ex: `RacesList.vue`), que gerenciam seu próprio estado (`data`), ciclo de vida (`created`) e métodos (`fetchRaces`).
- **CORS (Cross-Origin Resource Sharing)**: Configurado no `main.py` do FastAPI para autorizar explicitamente a origem do Vite (`http://localhost:5173`), permitindo que o navegador aceite as respostas da API sem bloqueios de segurança.

## 8. Estrutura Completa do Projeto (Fullstack)

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
│   │   ├── App.vue            # Componente raiz da aplicação
│   │   └── main.js            # Ponto de entrada do Vue
│   └── package.json           # Dependências do Node.js
├── criar_tabelas.py           # Script para gerar o schema no PostgreSQL
├── main.py                    # Ponto de entrada da aplicação FastAPI (com CORS)
├── requirements.txt           # Dependências Python
└── .env                       # Variáveis de ambiente (não versionado)
