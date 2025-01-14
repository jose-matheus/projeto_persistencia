from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# Modelo de Consulta
class Consulta(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    paciente_id: int
    medico_id: int = Field(foreign_key="medico.id")  # Relacionando com Medico
    data_hora: datetime
    status: str  # Exemplo: "Agendada", "Cancelada", "Concluída"
    observacoes: str = ""

    # Relacionamento com Medico
    medico: "Medico" = Relationship(back_populates="consultas")

# Pydantic schema para criação de consulta
class ConsultaCreate(SQLModel):
    paciente_id: int
    medico_id: int
    data_hora: datetime
    status: str
    observacoes: str = ""
