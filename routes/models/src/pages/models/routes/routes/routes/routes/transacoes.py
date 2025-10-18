from fastapi import APIRouter, Depends
from models.transacao import Transacao
from database import SessionLocal
from schemas import TransacaoCreate

router = APIRouter(prefix="/transacoes")

@router.post("/deposito")
def deposito(transacao: TransacaoCreate, db=Depends(SessionLocal)):
    conta = db.query(Conta).filter(Conta.numero == transacao.conta_numero).first()
    conta.saldo += transacao.valor
    nova = Transacao(tipo="depósito", valor=transacao.valor, conta_numero=conta.numero)
    db.add(nova)
    db.commit()
    return {"mensagem": "Depósito realizado"}
