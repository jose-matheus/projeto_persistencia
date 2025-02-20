from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.paciente import Paciente


class Consulta(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    paciente_id: int = Field(foreign_key="paciente.id")
    medico_id: int = Field(default=None, foreign_key="medico.id")
    data_hora: datetime
    status: str  # Exemplo: "Agendada", "Cancelada", "Concluída"
    observacoes: str = ""
   
    paciente: "Paciente" = Relationship(back_populates="consultas")
    medico: "Medico" = Relationship(back_populates="consultas")

class ConsultaCreate(SQLModel):
    paciente_id: int
    medico_id: int
    data_hora: datetime
    status: str
    observacoes: str = ""

