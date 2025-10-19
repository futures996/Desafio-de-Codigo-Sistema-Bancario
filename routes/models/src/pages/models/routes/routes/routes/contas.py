from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.conta import Conta
from schemas.conta import ContaCreate
from auth import verificar_token

router = APIRouter(prefix="/contas", dependencies=[Depends(verificar_token)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def criar_conta(conta: ContaCreate, db: Session = Depends(get_db)):
    if db.query(Conta).filter(Conta.numero == conta.numero).first():
        raise HTTPException(status_code=400, detail="Conta já existe")
    nova = Conta(**conta.dict())
    db.add(nova)
    db.commit()
    return {"mensagem": "Conta criada com sucesso"}

@router.get("/{numero}")
def consultar_conta(numero: str, db: Session = Depends(get_db)):
    conta = db.query(Conta).filter(Conta.numero == numero).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return conta
