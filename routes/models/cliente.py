from pydantic import BaseModel

class Cliente(BaseModel):
    nome: str
    cpf: str
    senha: str
