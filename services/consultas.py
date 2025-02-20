from sqlmodel import Session, select
from models.consultas import Consulta, ConsultaCreate
from models.medicos import Medico
from models.paciente import Paciente
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime

#Função para adicionar consulta no banco de dados
def adicionar_consulta_db(consulta: ConsultaCreate, db: Session) -> Consulta:
    medico = db.query(Medico).filter(Medico.id == consulta.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db_consulta = Consulta(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

#Função para listar todas as consultas
def listar_consultas_db(db: Session):
    consultas = db.query(Consulta).all()
    return {
        "consultas": consultas,
        "quantidade": len(consultas)
    }

#Função para buscar consulta por ID
def buscar_consulta_por_id_db(id: int, db: Session) -> Consulta:
    consulta = db.query(Consulta).filter(Consulta.id == id).first()
    return consulta

#Função para atualizar consulta no banco de dados
def atualizar_consulta_db(id: int, consulta: ConsultaCreate, db: Session) -> Consulta:
    medico = db.query(Medico).filter(Medico.id == consulta.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db_consulta = db.query(Consulta).filter(Consulta.id == id).first()

    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    for key, value in consulta.dict(exclude_unset=True).items():
        setattr(db_consulta, key, value)

    db.commit()
    db.refresh(db_consulta)

    return db_consulta

#Função para excluir consulta no banco de dados
def excluir_consulta_db(id: int, db: Session) -> bool:
    db_consulta = db.query(Consulta).filter(Consulta.id == id).first()
    if db_consulta:
        db.delete(db_consulta)
        db.commit()
        return True
    return False
    
#Função para listaras consultas do paciente
def listar_consultas_por_paciente_db(paciente_id: int, db: Session):
    return db.query(Consulta).filter(Consulta.paciente_id == paciente_id).all()

#Função para listar os pacientes sem consultas
def listar_pacientes_sem_consultas_db(db: Session):
    return db.query(Paciente).outerjoin(Consulta, Paciente.id == Consulta.paciente_id)\
             .filter(Consulta.id == None).all()

#Função para listar todas as consultas dentro de um periodo
def listar_consultas_por_periodo_db(inicio: datetime, fim: datetime, db: Session):
    consultas = db.query(Consulta).filter(
        Consulta.data_hora >= inicio,
        Consulta.data_hora <= fim
    ).all()
    return consultas


def listar_consultas_com_pacientes(medico_id: int, db: Session) -> list[dict]:
    statement = select(Consulta).join(Consulta.medico).where(Medico.id == medico_id)
    consultas = db.exec(statement).all()

    resultado = []
    
    for consulta in consultas:
        consulta_info = {
            "consulta_id": consulta.id,
            "paciente": consulta.paciente.nome,
            "status": consulta.status,
            "data": consulta.data_hora
        }
        resultado.append(consulta_info)
    
    return resultado