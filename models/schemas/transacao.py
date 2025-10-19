from pydantic import BaseModel

class TransacaoCreate(BaseModel):
    tipo: str
    valor: float
    conta_origem: str
    conta_destino: str | None = None
