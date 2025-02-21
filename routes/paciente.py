from fastapi import APIRouter, HTTPException, Query, Depends
from beanie import PydanticObjectId
from services.paciente import (
    criar_paciente_db,
    listar_pacientes_db,
    obter_paciente_db,
    atualizar_paciente_db,
    deletar_paciente_db,
    obter_paciente_com_consultas_db
)
from models.paciente import PacienteCreate, PacienteRetorno, PacienteComConsultas
from database.database import get_db

router = APIRouter(tags = ["Pacientes"])

# Rota para criar paciente
@router.post("/pacientes/", response_model=PacienteRetorno)
async def criar_paciente(paciente: PacienteCreate):
    try:
        return await criar_paciente_db(paciente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar paciente: {str(e)}")

# Rota para listar pacientes
@router.get("/pacientes/", response_model=list[PacienteRetorno])
async def listar_pacientes(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db=Depends(get_db)):
    try:
        # Chama o service passando os parâmetros de paginação
        pacientes = await listar_pacientes_db(skip, limit)
        return pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pacientes: {str(e)}")

# Rota para obter paciente pelo ID
@router.get("/pacientes/{id}", response_model=PacienteRetorno)
async def obter_paciente(id: str):
    try:
        paciente = await obter_paciente_db(id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return paciente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter paciente: {str(e)}")

# Rota para atualizar paciente
@router.put("/pacientes/{id}", response_model=PacienteRetorno)
async def atualizar_paciente(id: str, paciente: PacienteCreate):
    try:
        paciente_atualizado = await atualizar_paciente_db(id, paciente)
        if not paciente_atualizado:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return paciente_atualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar paciente: {str(e)}")

# Rota para deletar paciente
@router.delete("/pacientes/{id}")
async def deletar_paciente(id: str):
    try:
        if not await deletar_paciente_db(id):
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return {"msg": "Paciente deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar paciente: {str(e)}")

# Rota para listar os pacientes com suas consultas    
@router.get("/pacientes/{id}/consultas", response_model=PacienteComConsultas)
async def obter_paciente_com_consultas(id: str):
    try:
        paciente = await obter_paciente_com_consultas_db(id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        return paciente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter paciente com consultas: {str(e)}")

