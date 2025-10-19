from sqlalchemy import Column, String, Float, ForeignKey
from database import Base

class Conta(Base):
    __tablename__ = "contas"
    numero = Column(String, primary_key=True, index=True)
    tipo = Column(String)
    saldo = Column(Float, default=0.0)
    cliente_cpf = Column(String, ForeignKey("clientes.cpf"))
