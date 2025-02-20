from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from models.consultas import Consulta

if TYPE_CHECKING:
    from models.consultas import Consulta

class PacienteBase(BaseModel):
    nome: str
    telefone: str
    email: Optional[EmailStr]
    sexo: Optional[str]  # 'M', 'F' ou 'Outro'
    peso: Optional[float]
    altura: Optional[float]
    problemas_de_saude: Optional[str]

class PacienteCreate(PacienteBase):
    pass

class PacienteRetorno(PacienteBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True

# Tabela para o relacionamento entre Paciente e Médico
class PacienteMedico(SQLModel, table=True):
    paciente_id: int = Field(foreign_key="paciente.id", primary_key=True)
    medico_id: int = Field(foreign_key="medico.id", primary_key=True)

class Paciente(PacienteBase, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.utcnow)

    consultas: List["Consulta"] = Relationship(back_populates="paciente")
    
    medicos: List["Medico"] = Relationship(back_populates="pacientes", link_model=PacienteMedico)  # link_model faz a ligação com PacienteMedico

class PacienteComConsultas(PacienteRetorno):
    consultas: List["Consulta"]
