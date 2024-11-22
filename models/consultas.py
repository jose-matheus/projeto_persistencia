from pydantic import BaseModel
from datetime import datetime

class Consulta(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    data_hora: datetime
    status: str  # Exemplo: "Agendada", "Cancelada", "Concluída"
    observacoes: str = ""
