from fastapi import FastAPI
from routes import clientes, contas, transacoes

app = FastAPI(title="Sistema Bancário Web")

app.include_router(clientes.router)
app.include_router(contas.router)
app.include_router(transacoes.router)
