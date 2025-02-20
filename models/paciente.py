from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from beanie import Document
from models.consultas import objectid_to_str


# Modelo base de Paciente
class PacienteBase(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome: str
    telefone: str
    email: Optional[EmailStr]
    sexo: Optional[str]  # 'M', 'F' ou 'Outro'
    peso: Optional[float]
    altura: Optional[float]
    problemas_de_saude: Optional[str]
    data_criacao: Optional[datetime]

    class Config:
        from_attributes = True  # Facilita a conversão de objetos do banco para o modelo Pydantic

# Modelo para criação de paciente
class PacienteCreate(PacienteBase):
    pass

# Modelo para retorno de paciente
class PacienteRetorno(PacienteBase):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    data_criacao: Optional[datetime]

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed=True
        json_encoders = {
            ObjectId: str
        }

# Modelo Beanie para paciente com acesso ao MongoDB
class Paciente(PacienteBase, Document):
    id: str  # ID no MongoDB
    data_criacao: Optional[datetime] = Field(default_factory=datetime.utcnow)

    consultas: List[str] = []  # Lista de ObjectId das consultas
    medicos: List[str] = []  # Lista de ObjectId dos médicos

    class Settings:
        collection = "pacientes"  # Nome da coleção no MongoDB

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed=True
        json_encoders = {
            ObjectId: str
        }

# Modelo que inclui consultas para pacientes
class PacienteComConsultas(PacienteRetorno):
    consultas: List[str] = [] # Agora armazena ObjectIds das consultas

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed=True
        json_encoders = {
            ObjectId: str
        }