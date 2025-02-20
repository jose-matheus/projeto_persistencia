from fastapi import APIRouter, Depends, HTTPException, Query
from models.consultas import ConsultaCreate, Consulta, ConsultaResponse
from models.paciente import Paciente
from services.consultas import (
    adicionar_consulta_db, listar_consultas_db, buscar_consulta_por_id_db,
    atualizar_consulta_db, excluir_consulta_db, listar_consultas_por_paciente_db,
    listar_pacientes_sem_consultas_db, listar_consultas_por_periodo_db,
    listar_consultas_com_pacientes
)
from database.database import get_db  # Função que retorna a conexão assíncrona do Beanie.
from datetime import datetime
from typing import List
from beanie import PydanticObjectId

router = APIRouter()

# Rota para criar a consulta
@router.post("/consultas/", response_model=Consulta)
async def criar_consulta(consulta: ConsultaCreate):
    try:
        return await adicionar_consulta_db(consulta)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar consulta: {str(e)}")

# Rota para listar as consultas
@router.get("/consultas/", response_model=ConsultaResponse)
async def listar_consultas():
    try:
        return await listar_consultas_db()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar consultas: {str(e)}")

# Rota para obter a consulta pelo ID
@router.get("/consultas/{id}", response_model=Consulta)
async def buscar_consulta(id: str):
    try:
        consulta = await buscar_consulta_por_id_db(id)
        if not consulta:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        return consulta
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consulta: {str(e)}")

# Rota para atualizar uma consulta
@router.put("/consultas/{id}", response_model=Consulta)
async def atualizar_consulta(id: str, consulta: ConsultaCreate):
    try:
        consulta_atualizada = await atualizar_consulta_db(id, consulta)
        if not consulta_atualizada:
            raise HTTPException(status_code=404, detail="Consulta não encontrada.")
        return consulta_atualizada
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar consulta: {str(e)}")

# Rota para deletar uma consulta
@router.delete("/consultas/{id}", response_model=bool)
async def excluir_consulta(id: str):
    try:
        sucesso = await excluir_consulta_db(id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        return sucesso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir consulta: {str(e)}")

# Rota para listar as consultas pelo paciente
@router.get("/pacientes/{paciente_id}/consultas/", response_model=list[Consulta])
async def listar_consultas_por_paciente(paciente_id: str):
    try:
        consultas = await listar_consultas_por_paciente_db(paciente_id)
        if not consultas:
            raise HTTPException(status_code=404, detail="Nenhuma consulta encontrada para este paciente")
        return consultas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas: {str(e)}")
    

# Rota para listar todos os pacientes sem consultas
@router.get("/pacientes/sem-consultas/", response_model=list[Paciente])
async def listar_pacientes_sem_consultas():
    try:
        pacientes = await listar_pacientes_sem_consultas_db()
        if not pacientes:
            raise HTTPException(status_code=404, detail="Nenhum paciente sem consultas encontrado")
        return pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pacientes: {str(e)}")

# Rota para listar todas as consultas dentro de um periodo
@router.get("/consultas/periodo/", response_model=list[Consulta])
async def listar_consultas_por_periodo(
    inicio: datetime = Query(..., description="Data e hora de início no formato ISO8601"),
    fim: datetime = Query(..., description="Data e hora de fim no formato ISO8601")
):
    try:
        consultas = await listar_consultas_por_periodo_db(inicio, fim)
        if not consultas:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma consulta encontrada no período especificado."
            )
        return consultas
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar consultas: {str(e)}"
        )

# Rota para listar o paciente com todas as suas consultas
@router.get("/medico/{medico_id}/consultas/", response_model=list[dict])
async def consultar_consultas_pacientes(medico_id: str):
    try:
        consultas_com_pacientes = await listar_consultas_com_pacientes(medico_id)
        if not consultas_com_pacientes:
            raise HTTPException(status_code=404, detail="Nenhuma consulta encontrada para o médico.")
        return consultas_com_pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas: {str(e)}")
