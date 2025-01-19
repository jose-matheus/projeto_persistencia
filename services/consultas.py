from sqlmodel import Session
from models.consultas import Consulta, ConsultaCreate
from models.medicos import Medico  # Importando o modelo de Medico
from models.paciente import PacienteRetorno
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# Adicionar consulta no banco de dados
def adicionar_consulta_db(consulta: ConsultaCreate, db: Session) -> Consulta:
    # Verificar se o médico existe
    medico = db.query(Medico).filter(Medico.id == consulta.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    # Criar a consulta e adicioná-la ao banco
    db_consulta = Consulta(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

# Listar todas as consultas
def listar_consultas_db(db: Session):
    consultas = db.query(Consulta).all()
    return {
        "consultas": consultas,
        "quantidade": len(consultas)
    }

# Buscar consulta por ID
def buscar_consulta_por_id_db(id: int, db: Session) -> Consulta:
    consulta = db.query(Consulta).filter(Consulta.id == id).first()
    return consulta

# Atualizar consulta no banco de dados
def atualizar_consulta_db(id: int, consulta: ConsultaCreate, db: Session) -> Consulta:
    # Verificar se o médico existe
    medico = db.query(Medico).filter(Medico.id == consulta.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    # Buscar a consulta no banco
    db_consulta = db.query(Consulta).filter(Consulta.id == id).first()

    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    # Atualizar os dados da consulta
    for key, value in consulta.dict(exclude_unset=True).items():
        setattr(db_consulta, key, value)

    db.commit()
    db.refresh(db_consulta)

    return db_consulta

# Excluir consulta no banco de dados
def excluir_consulta_db(id: int, db: Session) -> bool:
    db_consulta = db.query(Consulta).filter(Consulta.id == id).first()
    if db_consulta:
        db.delete(db_consulta)
        db.commit()
        return True
    return False

def listar_consultas_por_paciente(paciente_id: int, db: Session):
    return db.query(Consulta).filter(Consulta.paciente_id == paciente_id).all()

def listar_pacientes_sem_consultas_db(db: Session):
    return db.query(Paciente).outerjoin(Consulta, Paciente.id == Consulta.paciente_id)\
             .filter(Consulta.id == None).all()