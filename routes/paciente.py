from fastapi import APIRouter, HTTPException
from models.paciente import PacienteCreate, Paciente
from services.paciente import criar_paciente

router = APIRouter()

@router.post("/pacientes/", response_model=Paciente)
async def criar_paciente_endpoint(paciente: PacienteCreate):
    try:
        return await criar_paciente(paciente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
