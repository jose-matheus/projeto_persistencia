from typing import List, Optional
from models.medicos import Medico

# Simulando um banco de dados na memória
medicos_db: List[Medico] = []

def criar_medico(medico: Medico) -> Medico:
    medicos_db.append(medico)
    return medico

def listar_medicos() -> List[Medico]:
    return medicos_db

def buscar_medico_por_id(id: int) -> Optional[Medico]:
    return next((m for m in medicos_db if m.id == id), None)
