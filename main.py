from models.cliente import Cliente
from models.conta import Conta
from services.autenticacao import gerar_hash_senha
from utils.auditoria import registrar_evento

# Exemplo de criação de cliente
senha_hash = gerar_hash_senha("senha123")
cliente = Cliente("Luan", "12345678901", senha_hash)

conta = Conta("0001", "corrente", saldo=1000.0)
cliente.contas.append(conta)

registrar_evento("criação", f"Cliente {cliente.nome} com conta {conta.numero} criada.")
