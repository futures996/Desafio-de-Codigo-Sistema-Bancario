from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.cliente import Cliente
from schemas.cliente import ClienteCreate
import bcrypt
from auth import criar_token

router = APIRouter(prefix="/clientes")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    hash_senha = bcrypt.hashpw(cliente.senha.encode(), bcrypt.gensalt())
    novo = Cliente(cpf=cliente.cpf, nome=cliente.nome, senha_hash=hash_senha)
    db.add(novo)
    db.commit()
    return {"mensagem": "Cliente criado com sucesso"}

@router.post("/login")
def login(cpf: str, senha: str, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.cpf == cpf).first()
    if not cliente or not bcrypt.checkpw(senha.encode(), cliente.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = criar_token({"sub": cliente.cpf})
    return {"access_token": token, "token_type": "bearer"}

