from fastapi import HTTPException, Depends
from datetime import datetime
from models.paciente import Paciente, PacienteCreate, PacienteComConsultas
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict
from models.consultas import Consulta
from beanie import PydanticObjectId
from bson import ObjectId
from typing import List

# Função para criar um paciente
async def criar_paciente_db(paciente: PacienteCreate) -> Paciente:
    db_paciente = Paciente(**paciente.dict())
    await db_paciente.insert()
    return db_paciente

# Função para listar todos os pacientes
async def listar_pacientes_db(skip: int = 0, limit: int = 10) -> List[Paciente]:
    try:
        # Aplica os parâmetros de paginação no banco de dados
        pacientes = await Paciente.find().skip(skip).limit(limit).to_list()
        return pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pacientes: {str(e)}")

# Função para obter um paciente pelo ID
async def obter_paciente_db(id: str) -> Paciente:
    db_paciente = await Paciente.get(id)
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

# Função para atualizar um paciente
async def atualizar_paciente_db(id: str, paciente: PacienteCreate) -> Paciente:
    paciente_db = await Paciente.get(id)
    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    # Atualiza o paciente com os dados fornecidos
    await paciente_db.update({"$set": paciente.dict(exclude_unset=True)})
    return paciente_db

# Função para deletar um paciente
async def deletar_paciente_db(id: str) -> bool:
    paciente = await Paciente.get(id)
    if not paciente:
        return False
    await paciente.delete()
    return True

# Função para listar o paciente com todas as suas consultas
async def obter_paciente_com_consultas_db(id: str) -> PacienteComConsultas:
    paciente = await Paciente.get(id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Assumindo que você tenha um relacionamento entre paciente e consultas
    consultas = await Consulta.find({"id": {"$in": paciente.consultas}}).to_list()


    paciente_dict = paciente.dict()
    paciente_dict.pop("consultas", None)  # Remove a chave 'consultas' se existir

    paciente_com_consultas = PacienteComConsultas(consultas=consultas, **paciente_dict)
    
    return paciente_com_consultas
