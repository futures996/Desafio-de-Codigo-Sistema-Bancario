from pydantic import BaseModel

class ContaCreate(BaseModel):
    numero: str
    tipo: str
    cliente_cpf: str
