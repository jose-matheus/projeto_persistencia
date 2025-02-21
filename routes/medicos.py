from fastapi import APIRouter, HTTPException, Query, Depends
from beanie import PydanticObjectId
from services.medicos import (
    criar_medico_db, listar_medicos_db, obter_medico_db, atualizar_medico_db,
    deletar_medico_db, obter_medico_por_nome_db, listar_medicos_por_especialidade_db,
    listar_pacientes_por_medico, associar_paciente_a_medico, contar_pacientes_por_medico
)
from models.medicos import MedicoCreate, MedicoRetorno
from database.database import get_db  # Função que retorna a conexão assíncrona do Beanie.
from typing import List, Dict

router = APIRouter(tags = ["Medicos"])

# Rota para criar médico
@router.post("/medicos/", response_model=MedicoRetorno)
async def criar_medico(medico: MedicoCreate):
    try:
        return await criar_medico_db(medico)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar médico: {str(e)}")

# Rota para listar médicos
@router.get("/medicos/", response_model=list[MedicoRetorno])
async def listar_medicos(skip: int = Query(0, ge=0), limit: int = Query(10, le=100)):
    try:
        # Chama a função de consulta no banco com os parâmetros de paginação
        medicos = await listar_medicos_db(skip=skip, limit=limit)
        return medicos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar médicos: {str(e)}")

# Rota para obter médico pelo ID
@router.get("/medicos/{id}", response_model=MedicoRetorno)
async def obter_medico(id: str):
    try:
        medico = await obter_medico_db(id)
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return medico
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter médico: {str(e)}")

# Rota para atualizar médico
@router.put("/medicos/{id}", response_model=MedicoRetorno)
async def atualizar_medico(id: str, medico: MedicoCreate):
    try:
        medico_atualizado = await atualizar_medico_db(id, medico)
        if not medico_atualizado:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return medico_atualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar médico: {str(e)}")

# Rota para deletar médico
@router.delete("/medicos/{id}")
async def deletar_medico(id: str):
    try:
        if not await deletar_medico_db(id):
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return {"msg": "Médico deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar médico: {str(e)}")

# Rota para obter médicos pelo nome
@router.get("/medicos/buscar_por_nome/", response_model=list[MedicoRetorno])
async def obter_medico_por_nome(nome: str):
    try:
        medicos = await obter_medico_por_nome_db(nome)
        if not medicos:
            raise HTTPException(status_code=404, detail="Nenhum médico encontrado com esse nome")
        return medicos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar médicos pelo nome: {str(e)}")

# Rota para listar médicos por especialidade com paginação
@router.get("/medicos/especialidade/", response_model=list[MedicoRetorno])
async def listar_medicos_por_especialidade(especialidade: str, skip: int = 0, limit: int = 10):
    try:
        medicos = await listar_medicos_por_especialidade_db(especialidade, skip, limit)
        if not medicos:
            raise HTTPException(status_code=404, detail="Nenhum médico encontrado para esta especialidade")
        return medicos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar médicos por especialidade: {str(e)}")

# Rota para listar todos os pacientes de um médico    
@router.get("/medicos/{medico_id}/pacientes", response_model=List[Dict])
async def obter_pacientes_por_medico(medico_id: str):
    pacientes = await listar_pacientes_por_medico(medico_id)
    if not pacientes:
        raise HTTPException(status_code=404, detail="Nenhum paciente encontrado para este médico.")
    return pacientes

# Rota para adicionar o paciente ao médico
@router.post("/medicos/{medico_id}/pacientes/{paciente_id}")
async def adicionar_paciente_ao_medico(paciente_id: str, medico_id: str):
    try:
        resultado = await associar_paciente_a_medico(paciente_id, medico_id)
        return {
            "msg": f"Paciente {resultado['paciente_nome']} foi associado ao médico {resultado['medico_nome']} com sucesso!"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/medicos/{id}/quantidade_pacientes")
async def get_quantidade_pacientes(id: str):
    try:
        quantidade = await contar_pacientes_por_medico(id)
        return {"id": id, "quantidade_pacientes": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar pacientes: {str(e)}")