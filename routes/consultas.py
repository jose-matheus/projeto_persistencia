from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.consultas import ConsultaCreate, Consulta
from models.paciente import Paciente
from services.consultas import (
    adicionar_consulta_db, listar_consultas_db, buscar_consulta_por_id_db,
    atualizar_consulta_db, excluir_consulta_db, listar_consultas_por_paciente_db,
    listar_pacientes_sem_consultas_db, listar_consultas_por_periodo_db,
    listar_consultas_com_pacientes
)
from database import get_db
from datetime import datetime


router = APIRouter()

# Rota para criar a consulta
@router.post("/consultas/", response_model=Consulta)
def criar_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    try:
        return adicionar_consulta_db(consulta, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar consulta: {str(e)}")

# Rota para listar as consultas
@router.get("/consultas/", response_model=dict)
def listar_consultas(db: Session = Depends(get_db)):
    try:
        return listar_consultas_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar consultas: {str(e)}")

# Rota para obter a constulta pelo ID
@router.get("/consultas/{id}", response_model=Consulta)
def buscar_consulta(id: int, db: Session = Depends(get_db)):
    try:
        consulta = buscar_consulta_por_id_db(id, db)
        if not consulta:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        return consulta
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consulta: {str(e)}")

# Rota para atualizar uma consulta
@router.put("/consultas/{id}", response_model=Consulta)
def atualizar_consulta(id: int, consulta: ConsultaCreate, db: Session = Depends(get_db)):
    try:
        consulta_atualizada = atualizar_consulta_db(id, consulta, db)
        
        if not consulta_atualizada:
            raise HTTPException(status_code=404, detail="Consulta não encontrada.")
        return consulta_atualizada
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar consulta: {str(e)}")

# Rota para deletar uma consulta
@router.delete("/consultas/{id}", response_model=bool)
def excluir_consulta(id: int, db: Session = Depends(get_db)):
    try:
        sucesso = excluir_consulta_db(id, db)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        return sucesso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir consulta: {str(e)}")

# Rota para listar as consultas pelo paciente
@router.get("/pacientes/{paciente_id}/consultas/", response_model=list[Consulta])
def listar_consultas_por_paciente(paciente_id: int, db: Session = Depends(get_db)):
    try:
        consultas = listar_consultas_por_paciente_db(paciente_id, db)
        if not consultas:
            raise HTTPException(status_code=404, detail="Nenhuma consulta encontrada para este paciente")
        return consultas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas: {str(e)}")

# Rota para listar todos os pacientes sem consultas
@router.get("/pacientes/sem-consultas/", response_model=list[Paciente])
def listar_pacientes_sem_consultas(db: Session = Depends(get_db)):
    try:
        pacientes = listar_pacientes_sem_consultas_db(db)
        if not pacientes:
            raise HTTPException(status_code=404, detail="Nenhum paciente sem consultas encontrado")
        return pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pacientes: {str(e)}")

# Rota para listar todas as consultas entre um periodo
@router.get("/consultas/periodo/", response_model=list[Consulta])
def listar_consultas_por_periodo(
    inicio: datetime = Query(..., description="Data e hora de início no formato ISO8601"),
    fim: datetime = Query(..., description="Data e hora de fim no formato ISO8601"),
    db: Session = Depends(get_db)
):
    try:
        consultas = listar_consultas_por_periodo_db(inicio, fim, db)
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
def consultar_consultas_pacientes(medico_id: int, db: Session = Depends(get_db)):
    try:
        consultas_com_pacientes = listar_consultas_com_pacientes(medico_id, db)
        if not consultas_com_pacientes:
            raise HTTPException(status_code=404, detail="Nenhuma consulta encontrada para o médico.")
        return consultas_com_pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas: {str(e)}")