from fastapi import FastAPI
from database import Base, engine
from routes import clientes

app = FastAPI(title="Sistema Bancário Web")
app.include_router(clientes.router)

Base.metadata.create_all(bind=engine)
