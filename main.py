from fastapi import FastAPI
from routes.paciente import router as paciente_router
from routes.medicos import router as medicos_router
from routes.consultas import router as consultas_router

app = FastAPI()

 # Inclui as rotas
app.include_router(paciente_router)
app.include_router(medicos_router)
app.include_router(consultas_router)
