from fastapi import APIRouter, HTTPException
from models.cliente import Cliente
from database import SessionLocal
from auth import criar_token

router = APIRouter(prefix="/login")

@router.post("/")
def login(cpf: str, senha: str):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.cpf == cpf, Cliente.senha == senha).first()
    if not cliente:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = criar_token({"sub": cliente.cpf})
    return {"access_token": token, "token_type": "bearer"}
