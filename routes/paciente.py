from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.paciente import (
    criar_paciente_db,
    listar_pacientes_db,
    obter_paciente_db,
    atualizar_paciente_db,
    deletar_paciente_db,
    obter_paciente_com_consultas_db
)
from models.paciente import PacienteCreate, PacienteRetorno, PacienteComConsultas
from database import get_db

router = APIRouter()

# Rota para criar paciente
@router.post("/pacientes/", response_model=PacienteRetorno)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    try:
        return criar_paciente_db(paciente, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar paciente: {str(e)}")

# Rota para listar pacientes
@router.get("/pacientes/", response_model=list[PacienteRetorno])
def listar_pacientes(db: Session = Depends(get_db)):
    try:
        return listar_pacientes_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pacientes: {str(e)}")

# Rota para obter paciente pelo ID
@router.get("/pacientes/{id}", response_model=PacienteRetorno)
def obter_paciente(id: int, db: Session = Depends(get_db)):
    try:
        paciente = obter_paciente_db(id, db)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return paciente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter paciente: {str(e)}")

# Rota para atualizar paciente
@router.put("/pacientes/{id}", response_model=PacienteRetorno)
def atualizar_paciente(id: int, paciente: PacienteCreate, db: Session = Depends(get_db)):
    try:
        paciente_atualizado = atualizar_paciente_db(id, paciente, db)
        if not paciente_atualizado:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return paciente_atualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar paciente: {str(e)}")

# Rota para deletar paciente
@router.delete("/pacientes/{id}")
def deletar_paciente(id: int, db: Session = Depends(get_db)):
    try:
        if not deletar_paciente_db(id, db):
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return {"msg": "Paciente deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar paciente: {str(e)}")

# Rota para listar os pacientes com suas consultas    
@router.get("/pacientes/{id}/consultas", response_model=PacienteComConsultas)
def obter_paciente_com_consultas(id: int, db: Session = Depends(get_db)):
    try:
        paciente = obter_paciente_com_consultas_db(id, db)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return paciente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter paciente com consultas: {str(e)}")
