from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.conta import Conta
from models.transacao import Transacao
from schemas.transacao import TransacaoCreate
from auth import verificar_token

router = APIRouter(prefix="/transacoes", dependencies=[Depends(verificar_token)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def realizar_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db)):
    origem = db.query(Conta).filter(Conta.numero == transacao.conta_origem).first()
    if not origem:
        raise HTTPException(status_code=404, detail="Conta de origem não encontrada")

    if transacao.tipo == "deposito":
        origem.saldo += transacao.valor
    elif transacao.tipo == "saque":
        if origem.saldo < transacao.valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        origem.saldo -= transacao.valor
    elif transacao.tipo == "transferencia":
        destino = db.query(Conta).filter(Conta.numero == transacao.conta_destino).first()
        if not destino:
            raise HTTPException(status_code=404, detail="Conta de destino não encontrada")
        if origem.saldo < transacao.valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        origem.saldo -= transacao.valor
        destino.saldo += transacao.valor
    else:
        raise HTTPException(status_code=400, detail="Tipo de transação inválido")

    registro = Transacao(**transacao.dict())
    db.add(registro)
    db.commit()
    return {"mensagem": "Transação realizada com sucesso"}
