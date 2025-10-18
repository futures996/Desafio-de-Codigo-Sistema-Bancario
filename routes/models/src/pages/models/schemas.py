from pydantic import BaseModel

class ClienteCreate(BaseModel):
    cpf: str
    nome: str
    senha: str
