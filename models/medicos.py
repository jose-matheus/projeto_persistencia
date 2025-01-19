from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from models.paciente import PacienteMedico  # Importando o link_model de PacienteMedico

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
        from_attributes = True

# Modelo do banco de dados para Medico
class Medico(MedicoBase, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.utcnow)  # Usa default_factory para garantir datetime

    # Relacionamento com consultas
    consultas: List["Consulta"] = Relationship(back_populates="medico")
    
    # Relacionamento muitos para muitos com Pacientes
    pacientes: List["Paciente"] = Relationship(back_populates="medicos", link_model=PacienteMedico)  # link_model faz a ligação com PacienteMedico
