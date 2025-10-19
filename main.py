from fastapi import FastAPI
from database import Base, engine
from routes import clientes, contas, transacoes

app = FastAPI(title="Sistema Bancário API")

app.include_router(clientes.router)
app.include_router(contas.router)
app.include_router(transacoes.router)

Base.metadata.create_all(bind=engine)
