from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.cliente import Cliente
from schemas import ClienteCreate

router = APIRouter(prefix="/clientes")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo = Cliente(**cliente.dict())
    db.add(novo)
    db.commit()
    return {"mensagem": "Cliente criado com sucesso"}
