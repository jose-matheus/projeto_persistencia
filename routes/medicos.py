from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.medicos import criar_medico_db, listar_medicos_db, obter_medico_db, atualizar_medico_db, deletar_medico_db
from models.medicos import MedicoCreate, MedicoRetorno
from database import get_db

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
