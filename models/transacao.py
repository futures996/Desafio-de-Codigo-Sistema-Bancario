from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    valor = Column(Float)
    conta_origem = Column(String, ForeignKey("contas.numero"))
    conta_destino = Column(String, ForeignKey("contas.numero"), nullable=True)
