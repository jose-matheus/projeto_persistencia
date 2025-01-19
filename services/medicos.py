from sqlalchemy.orm import Session
from models.medicos import Medico, MedicoCreate
from models.paciente import Paciente
from sqlmodel import select
from fastapi import HTTPException
from typing import List

# Função para criar um médico
def criar_medico_db(medico: MedicoCreate, db: Session) -> Medico:
    db_medico = Medico(**medico.dict())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

# Função para listar todos os médicos
def listar_medicos_db(db: Session):
    return db.execute(select(Medico)).scalars().all()

# Função para obter um médico pelo ID
def obter_medico_db(id: int, db: Session) -> Medico:
    return db.query(Medico).filter(Medico.id == id).first()

# Função para atualizar um médico
def atualizar_medico_db(id: int, medico: MedicoCreate, db: Session) -> Medico:
    db_medico = db.query(Medico).filter(Medico.id == id).first()
    if db_medico:
        for key, value in medico.dict().items():
            setattr(db_medico, key, value)
        db.commit()
        db.refresh(db_medico)
        return db_medico
    return None

# Função para deletar um médico
def deletar_medico_db(id: int, db: Session) -> bool:
    db_medico = db.query(Medico).filter(Medico.id == id).first()
    if db_medico:
        db.delete(db_medico)
        db.commit()
        return True
    return False

# Função para obter médicos pelo nome
def obter_medico_por_nome_db(nome: str, db: Session):
    return db.query(Medico).filter(Medico.nome.ilike(f"%{nome}%")).all()


def listar_medicos_por_especialidade_db(especialidade: str, db: Session):
    return db.query(Medico).filter(Medico.especialidade.ilike(f"%{especialidade}%")).all()

def listar_pacientes_por_medico(medico_id: int, db: Session) -> List[dict]:
    # Consulta para obter o médico e seus pacientes
    statement = select(Medico).where(Medico.id == medico_id)
    medico = db.exec(statement).one_or_none()  # Agora deve retornar um único objeto
    
    resultado = []
    
    # Para cada paciente do médico, pega as informações
    for paciente in medico.pacientes:  # Acessa a lista de pacientes do médico
        paciente_info = {
            "paciente_id": paciente.id,
            "nome": paciente.nome,
            "telefone": paciente.telefone,
            "email": paciente.email
        }
        resultado.append(paciente_info)
    
    return resultado


