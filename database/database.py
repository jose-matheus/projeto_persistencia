from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
from typing import AsyncGenerator
from beanie import init_beanie
from models.consultas import Consulta  # Ajuste de acordo com seus modelos importados
from models.medicos import Medico
from models.paciente import Paciente

# URL de conexão com o MongoDB
MONGO_URL = "mongodb://localhost:27017"  # Altere para o seu MongoDB URL se necessário
DB_NAME = "banco"  # Altere para o nome do seu banco

# Instância do cliente assíncrono MongoDB
client = AsyncIOMotorClient(MONGO_URL)

# Banco de dados
db = client[DB_NAME]

# Função para obter o banco de dados (assíncrona)
def get_db() -> AsyncGenerator:
    try:
        yield db
    finally:
        pass

# Função para inicializar o Beanie com a base de dados
async def init_database():
    await init_beanie(
        database=db,
        document_models=[Consulta, Medico, Paciente]  # Inclua todos os modelos que você usou no seu código
    )

# Função para criar ou inicializar coleções, caso necessário
async def criar_tabelas():
    # Não é necessário criar coleções explicitamente com o Beanie, pois ele já cria as coleções automaticamente
    # quando você começa a usar os documentos
    pass
