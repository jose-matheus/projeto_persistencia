# database/database.py

from sqlmodel import create_engine, Session, SQLModel

# Configuração do banco de dados (exemplo com SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"  # Caminho para o banco SQLite

# Criação do engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    SQLModel.metadata.create_all(bind=engine)

# Função para obter a sessão do banco de dados
def get_db():
    with Session(engine) as session:
        yield session
