from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Modelo base para Paciente
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
        orm_mode = True

# Modelo do banco de dados para Paciente
class Paciente(PacienteBase, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.utcnow)  # Data de criação padrão
