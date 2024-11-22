from fastapi import APIRouter, HTTPException
from typing import List
from models.consultas import Consulta
from services.consultas import criar_consulta, listar_consultas, buscar_consulta_por_id

router = APIRouter()

@router.post("/consultas/", response_model=Consulta)
def criar(consulta: Consulta):
    return criar_consulta(consulta)

@router.get("/consultas/", response_model=List[Consulta])
def listar():
    return listar_consultas()

@router.get("/consultas/{id}", response_model=Consulta)
def buscar(id: int):
    consulta = buscar_consulta_por_id(id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta
