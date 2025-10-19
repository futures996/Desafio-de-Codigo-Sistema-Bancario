from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.transacao import Transacao
from auth import verificar_token
from datetime import datetime

router = APIRouter(prefix="/extrato", dependencies=[Depends(verificar_token)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{conta}")
def extrato_filtrado(
    conta: str,
    tipo: str | None = Query(None),
    inicio: datetime | None = Query(None),
    fim: datetime | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Transacao).filter(Transacao.conta_origem == conta)
    if tipo:
        query = query.filter(Transacao.tipo == tipo)
    if inicio:
        query = query.filter(Transacao.id >= inicio.timestamp())
    if fim:
        query = query.filter(Transacao.id <= fim.timestamp())
    return query.all()
