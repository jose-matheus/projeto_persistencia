from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.consultas import ConsultaCreate, Consulta
from models.paciente import Paciente
from services.consultas import (
    adicionar_consulta_db, listar_consultas_db, buscar_consulta_por_id_db,
    atualizar_consulta_db, excluir_consulta_db, listar_consultas_por_paciente,
    listar_pacientes_sem_consultas_db
)
from database import get_db

router = APIRouter()

@router.post("/consultas/", response_model=Consulta)
def criar_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    try:
        # Tentar adicionar a consulta
        return adicionar_consulta_db(consulta, db)
    except HTTPException as e:
        # Levanta um erro se o médico não for encontrado
        raise e
    except Exception as e:
        # Erro geral ao criar a consulta
        raise HTTPException(status_code=500, detail=f"Erro ao criar consulta: {str(e)}")

@router.get("/consultas/", response_model=dict)
def listar_consultas(db: Session = Depends(get_db)):
    try:
        # Lista todas as consultas
        return listar_consultas_db(db)
    except Exception as e:
        # Erro geral ao listar consultas
        raise HTTPException(status_code=500, detail=f"Erro ao listar consultas: {str(e)}")

@router.get("/consultas/{id}", response_model=Consulta)
def buscar_consulta(id: int, db: Session = Depends(get_db)):
    try:
        # Busca a consulta pelo ID
        consulta = buscar_consulta_por_id_db(id, db)
        if not consulta:
            # Caso não encontre a consulta, retorna erro 404
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        return consulta
    except Exception as e:
        # Erro geral ao buscar a consulta
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consulta: {str(e)}")

@router.put("/consultas/{id}", response_model=Consulta)
def atualizar_consulta(id: int, consulta: ConsultaCreate, db: Session = Depends(get_db)):
    try:
        # Tentar atualizar a consulta
        consulta_atualizada = atualizar_consulta_db(id, consulta, db)
        
        if not consulta_atualizada:
            # Caso a consulta não seja encontrada, retorna erro 404
            raise HTTPException(status_code=404, detail="Consulta não encontrada.")
        return consulta_atualizada
    except HTTPException as e:
        # Levanta um erro se o médico não for encontrado
        raise e
    except Exception as e:
        # Erro geral ao atualizar a consulta
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar consulta: {str(e)}")

@router.delete("/consultas/{id}", response_model=bool)
def excluir_consulta(id: int, db: Session = Depends(get_db)):
    try:
        # Tenta excluir a consulta
        sucesso = excluir_consulta_db(id, db)
        if not sucesso:
            # Caso não encontre a consulta para excluir, retorna erro 404
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        return sucesso
    except Exception as e:
        # Erro geral ao excluir a consulta
        raise HTTPException(status_code=500, detail=f"Erro ao excluir consulta: {str(e)}")

@router.get("/pacientes/{paciente_id}/consultas/", response_model=list[Consulta])
def listar_consultas_por_paciente_endpoint(paciente_id: int, db: Session = Depends(get_db)):
    try:
        consultas = listar_consultas_por_paciente(paciente_id, db)
        if not consultas:
            raise HTTPException(status_code=404, detail="Nenhuma consulta encontrada para este paciente")
        return consultas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas: {str(e)}")

@router.get("/pacientes/sem-consultas/", response_model=list[Paciente])
def listar_pacientes_sem_consultas(db: Session = Depends(get_db)):
    try:
        pacientes = listar_pacientes_sem_consultas_db(db)
        if not pacientes:
            raise HTTPException(status_code=404, detail="Nenhum paciente sem consultas encontrado")
        return pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pacientes: {str(e)}")