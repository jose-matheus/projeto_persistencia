from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.medicos import criar_medico_db, listar_medicos_db, obter_medico_db, atualizar_medico_db, deletar_medico_db, obter_medico_por_nome_db, listar_medicos_por_especialidade_db, listar_pacientes_por_medico, associar_paciente_a_medico
from models.medicos import MedicoCreate, MedicoRetorno
from database import get_db
from typing import List, Dict

router = APIRouter()

# Rota para criar médico
@router.post("/medicos/", response_model=MedicoRetorno)
def criar_medico(medico: MedicoCreate, db: Session = Depends(get_db)):
    try:
        return criar_medico_db(medico, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar médico: {str(e)}")

# Rota para listar médicos
@router.get("/medicos/", response_model=list[MedicoRetorno])
def listar_medicos(db: Session = Depends(get_db)):
    try:
        return listar_medicos_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar médicos: {str(e)}")

# Rota para obter médico pelo ID
@router.get("/medicos/{id}", response_model=MedicoRetorno)
def obter_medico(id: int, db: Session = Depends(get_db)):
    try:
        medico = obter_medico_db(id, db)
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return medico
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter médico: {str(e)}")

# Rota para atualizar médico
@router.put("/medicos/{id}", response_model=MedicoRetorno)
def atualizar_medico(id: int, medico: MedicoCreate, db: Session = Depends(get_db)):
    try:
        medico_atualizado = atualizar_medico_db(id, medico, db)
        if not medico_atualizado:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return medico_atualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar médico: {str(e)}")

# Rota para deletar médico
@router.delete("/medicos/{id}")
def deletar_medico(id: int, db: Session = Depends(get_db)):
    try:
        if not deletar_medico_db(id, db):
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return {"msg": "Médico deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar médico: {str(e)}")

# Rota para obter médicos pelo nome
@router.get("/medicos/buscar_por_nome/", response_model=list[MedicoRetorno])
def obter_medico_por_nome(nome: str, db: Session = Depends(get_db)):
    try:
        # Chama a função correta do repositório ou serviço
        medicos = obter_medico_por_nome_db(nome, db)
        if not medicos:
            raise HTTPException(status_code=404, detail="Nenhum médico encontrado com esse nome")
        return medicos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar médicos pelo nome: {str(e)}")

@router.get("/medicos/especialidade/", response_model=list[MedicoRetorno])
def listar_medicos_por_especialidade(especialidade: str, db: Session = Depends(get_db)):
    try:
        medicos = listar_medicos_por_especialidade_db(especialidade, db)
        if not medicos:
            raise HTTPException(status_code=404, detail="Nenhum médico encontrado para esta especialidade")
        return medicos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar médicos por especialidade: {str(e)}")
    
@router.get("/medicos/{medico_id}/pacientes", response_model=List[Dict])
def obter_pacientes_por_medico(medico_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para listar os pacientes de um médico específico.

    :param medico_id: ID do médico.
    :param db: Sessão do banco de dados.
    :return: Lista de pacientes do médico.
    """
    pacientes = listar_pacientes_por_medico(medico_id, db)
    if not pacientes:
        raise HTTPException(status_code=404, detail="Nenhum paciente encontrado para este médico.")
    return pacientes

@router.post("/medicos/{medico_id}/pacientes/{paciente_id}")
def adicionar_paciente_ao_medico(
    paciente_id: int,
    medico_id: int,
    db: Session = Depends(get_db)
):
    try:
        paciente_associado = associar_paciente_a_medico(paciente_id, medico_id, db)
        return {"msg": f"Paciente {paciente_associado.nome} foi associado ao médico com sucesso!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))