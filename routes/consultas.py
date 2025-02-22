from fastapi import APIRouter, Depends, HTTPException, Query
from models.consultas import ConsultaCreate, Consulta, ConsultaResponse
from models.paciente import Paciente
from services.consultas import (
    adicionar_consulta_db, listar_consultas_db, buscar_consulta_por_id_db,
    atualizar_consulta_db, excluir_consulta_db, listar_consultas_por_paciente_db,
    listar_pacientes_sem_consultas_db, listar_consultas_por_periodo_db,
    listar_consultas_com_pacientes, contar_consultas_por_paciente, calcular_media_tempo_entre_consultas
)
from database.database import get_db  # Função que retorna a conexão assíncrona do Beanie.
from datetime import datetime
from typing import List
from beanie import PydanticObjectId

router = APIRouter(tags = ["Consultas"])

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
async def listar_consultas(skip: int = Query(0, ge=0), limit: int = Query(10, le=100)):
    try:
        # Chama a função de consulta no banco com os parâmetros de paginação
        return await listar_consultas_db(skip=skip, limit=limit)
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
async def listar_consultas_por_paciente(paciente_id: str, skip: int = Query(0, ge=0), limit: int = Query(10, le=100)):
    try:
        consultas = await listar_consultas_por_paciente_db(paciente_id, skip, limit)
        if not consultas:
            raise HTTPException(status_code=404, detail="Nenhuma consulta encontrada para este paciente")
        return consultas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas: {str(e)}")
    

# Rota para listar todos os pacientes sem consultas
@router.get("/pacientes/sem-consultas/", response_model=list[Paciente])
async def listar_pacientes_sem_consultas(skip: int = Query(0, ge=0), limit: int = Query(10, le=100)):
    try:
        pacientes = await listar_pacientes_sem_consultas_db(skip, limit)
        if not pacientes:
            raise HTTPException(status_code=404, detail="Nenhum paciente sem consultas encontrado")
        return pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pacientes: {str(e)}")

# Rota para listar todas as consultas dentro de um periodo
@router.get("/consultas/periodo/")
async def listar_consultas_por_periodo(
    inicio: datetime = Query(..., description="Data e hora de início no formato ISO8601"),
    fim: datetime = Query(..., description="Data e hora de fim no formato ISO8601")
):
    try:
        resultado = await listar_consultas_por_periodo_db(inicio, fim)
        if not resultado["consultas"]:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma consulta encontrada no período especificado."
            )
        return resultado  # Retorna o dicionário com 'consultas' e 'contagem'
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar consultas: {str(e)}"
        )
    
@router.get("/pacientes/{id}/contagem_consultas")
async def contagem_consultas(id: str):
    try:
        contagem = await contar_consultas_por_paciente(id)
        return {"id": id, "contagem_consultas": contagem}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar consultas: {str(e)}")

@router.get("/pacientes/{id}/media_tempo_consultas")
async def media_tempo_consultas(id: str):
    try:
        media = await calcular_media_tempo_entre_consultas(id)
        return {"id": id, "media_tempo_consultas": media}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular média de tempo entre consultas: {str(e)}")
    
