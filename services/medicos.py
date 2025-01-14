from sqlalchemy.orm import Session
from models.medicos import Medico, MedicoCreate
from sqlmodel import select

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
