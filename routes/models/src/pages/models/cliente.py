from sqlalchemy import Column, String
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    cpf = Column(String, primary_key=True, index=True)
    nome = Column(String)
    senha = Column(String)
