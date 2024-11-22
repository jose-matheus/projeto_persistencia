from fastapi import APIRouter, HTTPException
from typing import List
from models.medicos import Medico
from services.medicos import criar_medico, listar_medicos, buscar_medico_por_id

router = APIRouter()

@router.post("/medicos/", response_model=Medico)
def criar(medico: Medico):
    return criar_medico(medico)

@router.get("/medicos/", response_model=List[Medico])
def listar():
    return listar_medicos()

@router.get("/medicos/{id}", response_model=Medico)
def buscar(id: int):
    medico = buscar_medico_por_id(id)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico
