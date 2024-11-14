from models.paciente import PacienteCreate, Paciente
from typing import List

# Lista simulando um banco de dados
fake_db: List[Paciente] = []

async def criar_paciente(paciente: PacienteCreate) -> Paciente:
    # Criação de um novo paciente (simulação de um banco de dados)
    novo_paciente = Paciente(
        id=len(fake_db) + 1,  # ID gerado automaticamente
        nome=paciente.nome,
        data_nascimento=paciente.data_nascimento,
        telefone=paciente.telefone,
        endereco=paciente.endereco,
        email=paciente.email,
        cpf=paciente.cpf,
        historico_medico=paciente.historico_medico,
        status=paciente.status
    )
    
    fake_db.append(novo_paciente)  # Simulando o "salvamento" no banco de dados
    return novo_paciente
