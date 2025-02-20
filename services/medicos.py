from sqlalchemy.orm import Session
from models.medicos import Medico, MedicoCreate
from models.paciente import Paciente, PacienteMedico
from sqlmodel import select
from fastapi import HTTPException
from typing import List, Dict

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

#Função para listar os médicos por especialidade
def listar_medicos_por_especialidade_db(especialidade: str, db: Session):
    return db.query(Medico).filter(Medico.especialidade.ilike(f"%{especialidade}%")).all()

#Função para listar os pacientes de um médico
def listar_pacientes_por_medico(medico_id: int, db: Session) -> List[Dict]:
    statement = select(Paciente).join(PacienteMedico).where(PacienteMedico.medico_id == medico_id)
    pacientes = db.exec(statement).all()

    if not pacientes:
        return [] 

    resultado = [
        {
            "paciente_id": paciente.id,
            "nome": paciente.nome,
            "telefone": paciente.telefone,
            "email": paciente.email,
        }
        for paciente in pacientes
    ]

    return resultado

#Função que vai associar o paciente ao médico da sua consulta
def associar_paciente_a_medico(paciente_id: int, medico_id: int, db: Session):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    
    if not paciente:
        raise ValueError(f"Paciente com ID {paciente_id} não encontrado.")
    if not medico:
        raise ValueError(f"Médico com ID {medico_id} não encontrado.")
    
    if medico in paciente.medicos:
        raise ValueError(f"Paciente {paciente.nome} já está associado ao médico {medico.nome}.")
    
    paciente.medicos.append(medico)
    
    db.add(paciente)
    db.commit()
    
    return paciente