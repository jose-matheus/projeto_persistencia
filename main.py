from fastapi import FastAPI
from database.database import init_database  # Importando a função de inicialização do Beanie
from routes.paciente import router as pacientes_router
from routes.consultas import router as consultas_router
from routes.medicos import router as medicos_router
import uvicorn

app = FastAPI()

# Inicializando o banco de dados com Beanie
@app.on_event("startup")
async def startup_db():
    await init_database()  # Inicializa a conexão com o banco de dados e o Beanie

# Incluindo as rotas
app.include_router(pacientes_router)
app.include_router(consultas_router)
app.include_router(medicos_router)

