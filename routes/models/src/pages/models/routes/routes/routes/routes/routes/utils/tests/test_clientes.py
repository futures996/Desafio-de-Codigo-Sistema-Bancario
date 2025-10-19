from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_criar_cliente():
    resposta = client.post("/clientes/", json={
        "cpf": "12345678900",
        "nome": "Luan",
        "senha": "senha123"
    })
    assert resposta.status_code == 200
    assert "mensagem" in resposta.json()
