from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# Pydantic model para validação
class PacienteCreate(BaseModel):
    nome: str
    data_nascimento: date
    telefone: str
    endereco: str
    email: EmailStr
    cpf: str
    historico_medico: Optional[List[str]] = []
    status: bool = True

# Pydantic model para o retorno do paciente (com id)
class Paciente(PacienteCreate):
    id: int

    class Config:
        orm_mode = True
