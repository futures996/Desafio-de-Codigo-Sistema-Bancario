from fastapi import APIRouter, Depends
from models.conta import Conta
from database import SessionLocal
from schemas import ContaCreate

router = APIRouter(prefix="/contas")

@router.post("/")
def criar_conta(conta: ContaCreate, db=Depends(SessionLocal)):
    nova = Conta(**conta.dict())
    db.add(nova)
    db.commit()
    return {"mensagem": "Conta criada"}
