# main.py
from fastapi import FastAPI
from database import criar_tabelas, get_db
from routes.paciente import router as pacientes_router
from routes.consultas import router as consultas_router
from routes.medicos import router as medicos_router

# Criação das tabelas no banco de dados
criar_tabelas()

app = FastAPI()


# Incluindo as rotas
app.include_router(pacientes_router)
app.include_router(consultas_router)
app.include_router(medicos_router)