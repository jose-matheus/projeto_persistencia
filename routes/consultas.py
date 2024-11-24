from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from models.consultas import Consulta
from services.consultas import (adicionar_consulta_csv, listar_consultas_csv, buscar_consulta_por_id,
                                 atualizar_consulta_csv, excluir_consulta_csv, 
                                 compactar_csv_em_zip, obter_hash_sha256_csv)

router = APIRouter()

# Rota para criar uma consulta
@router.post("/consultas/", response_model=Consulta)
def criar_consulta(consulta: Consulta):
    return adicionar_consulta_csv(consulta)

# Rota para listar todas as consultas e a quantidade delas
@router.get("/consultas/", response_model=dict)
def listar_consultas():
    return listar_consultas_csv()



# Rota para buscar uma consulta por ID
@router.get("/consultas/{id}", response_model=Consulta)
def buscar_consulta(id: int):
    consulta = buscar_consulta_por_id(id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta

# Rota para atualizar uma consulta
@router.put("/consultas/{id}", response_model=Consulta)
def atualizar_consulta(id: int, consulta: Consulta):
    consulta_atualizada = atualizar_consulta_csv(id, consulta)
    if not consulta_atualizada:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta_atualizada

# Rota para excluir uma consulta
@router.delete("/consultas/{id}", response_model=bool)
def excluir_consulta(id: int):
    sucesso = excluir_consulta_csv(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return sucesso


@router.get("/consultas/download/zip", response_class=StreamingResponse)
def baixar_zip_csv():
    zip_buffer = compactar_csv_em_zip()
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=consultas.zip"})



@router.get("/consultas/arquivo/hash", response_model=str)
def obter_hash():
    return obter_hash_sha256_csv()

