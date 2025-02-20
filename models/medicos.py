from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from models.paciente import PacienteMedico 


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
        from_attributes = True

class Medico(MedicoBase, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.utcnow) 

    consultas: List["Consulta"] = Relationship(back_populates="medico")
    
    
    pacientes: List["Paciente"] = Relationship(back_populates="medicos", link_model=PacienteMedico)
