from pydantic import BaseModel, EmailStr
from typing import List
from datetime import date

class Medico(BaseModel):
    id: int
    nome: str
    crm: str  # Conselho Regional de Medicina
    especialidade: str
    telefone: str
    email: EmailStr
    status: bool = True
