from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='Projetos API Corridas com FastAPI')

app.include_router(api_router, prefix='/api/v1')

# Configurações do CORS
origins = [
    "http://localhost:8081",  # URL do frontend Vue.js
    "http://localhost:8080",  # Alternativa
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
