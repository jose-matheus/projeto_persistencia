from typing import List, Optional
from models.consultas import Consulta

# Simulando um banco de dados na memória
consultas_db: List[Consulta] = []

def criar_consulta(consulta: Consulta) -> Consulta:
    consultas_db.append(consulta)
    return consulta

def listar_consultas() -> List[Consulta]:
    return consultas_db

def buscar_consulta_por_id(id: int) -> Optional[Consulta]:
    return next((c for c in consultas_db if c.id == id), None)
