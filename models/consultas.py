from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from beanie import Document
from typing import List

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


# Define o modelo de dados base
class ConsultaBase(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    paciente_id: str  # Armazena o ObjectId do paciente como string
    medico_id: str  # Armazena o ObjectId do médico como string
    data_hora: datetime
    status: str  # Exemplo: "Agendada", "Cancelada", "Concluída"
    observacoes: Optional[str] = ""

# Modelo para criação de consultas
class ConsultaCreate(ConsultaBase):
    pass

# Modelo Beanie para consulta com acesso ao MongoDB
class Consulta(ConsultaBase, Document):
    id: str  # ID no formato ObjectId

    class Settings:
        collection = "consultas"  # Nome da coleção no MongoDB

    class Config:
        populate_by_name = True  # Permite usar "_id" como "id"
        from_attributes = True  # Converte MongoDB dict para Pydantic
        arbitrary_types_allowed=True
        json_encoders = {
            ObjectId: str
        }

class ConsultaResponse(BaseModel):
    consultas: List[Consulta]  # Defina corretamente sua classe `Consulta`
    quantidade: int