from sqlalchemy.orm import Session
from models.paciente import Paciente, PacienteCreate, PacienteComConsultas
from sqlmodel import select
from sqlalchemy.orm import joinedload

# Função para criar um paciente
def criar_paciente_db(paciente: PacienteCreate, db: Session) -> Paciente:
    db_paciente = Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# Função para listar todos os pacientes
def listar_pacientes_db(db: Session):
    return db.execute(select(Paciente)).scalars().all()

# Função para obter um paciente pelo ID
def obter_paciente_db(id: int, db: Session) -> Paciente:
    return db.query(Paciente).filter(Paciente.id == id).first()

# Função para atualizar um paciente
def atualizar_paciente_db(id: int, paciente: PacienteCreate, db: Session) -> Paciente:
    db_paciente = db.query(Paciente).filter(Paciente.id == id).first()
    if db_paciente:
        for key, value in paciente.dict().items():
            setattr(db_paciente, key, value)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    return None

# Função para deletar um paciente
def deletar_paciente_db(id: int, db: Session) -> bool:
    db_paciente = db.query(Paciente).filter(Paciente.id == id).first()
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
        return True
    return False

#Função para listar o paciente com todas as suas consultas usando o JoinedLoad
def obter_paciente_com_consultas_db(id: int, db: Session) -> Paciente:
    return (
        db.query(Paciente)
        .options(joinedload(Paciente.consultas))
        .filter(Paciente.id == id)
        .first()
    )
