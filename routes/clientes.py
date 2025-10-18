from fastapi import APIRouter
from models import Cliente

router = APIRouter(prefix="/clientes")

@router.post("/")
def criar_cliente(cliente: Cliente):
    # lógica de criação
    return {"mensagem": "Cliente criado com sucesso"}
