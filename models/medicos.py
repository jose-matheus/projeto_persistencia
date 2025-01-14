from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

# Modelo base para o Médico
class MedicoBase(BaseModel):
    nome: str
    especialidade: str
    crm: str
    email: EmailStr
    telefone: str

class MedicoCreate(MedicoBase):
    pass

class MedicoRetorno(MedicoBase):
    id: int

    class Config:
        orm_mode = True

# Modelo do banco de dados para Medico
class Medico(MedicoBase, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.utcnow)  # Usa default_factory para garantir datetime

    # Relacionamento com consultas
    consultas: List["Consulta"] = Relationship(back_populates="medico")
