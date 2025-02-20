from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from beanie import Document
from models.consultas import objectid_to_str

# Define o modelo de dados base
class MedicoBase(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome: str
    especialidade: str
    crm: str
    email: EmailStr
    telefone: str

# Modelo para criação de médicos
class MedicoCreate(MedicoBase):
    pass

# Modelo para retorno de médicos
class MedicoRetorno(MedicoBase):
    id: str  # MongoDB usa string para ObjectId

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed=True
        json_encoders = {
            ObjectId: str
        }

# Modelo Beanie para médico com acesso ao MongoDB
class Medico(MedicoBase, Document):
    id: str  # ID no MongoDB
    data_criacao: datetime = Field(default_factory=datetime.utcnow)

    consultas: List[str] = [] # Lista de ObjectId das consultas
    pacientes: List[str] = []  # Lista de ObjectId dos pacientes

    class Settings:
        collection = "medicos"  # Nome da coleção no MongoDB

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed=True
        json_encoders = {
            ObjectId: str
        }
