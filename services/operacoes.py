from utils.validacoes import validar_valor
from utils.auditoria import registrar_evento
from models.transacao import Transacao

def depositar(conta, valor):
    validar_valor(valor)
    conta.saldo += valor
    transacao = Transacao("depósito", valor, f"Depósito de R${valor:.2f}")
    conta.transacoes.append(transacao)
    registrar_evento("depósito", f"Conta {conta.numero} recebeu R${valor:.2f}")

def sacar(conta, valor):
    validar_valor(valor)
    if valor > conta.saldo:
        raise ValueError("Saldo insuficiente.")
    conta.saldo -= valor
    transacao = Transacao("saque", valor, f"Saque de R${valor:.2f}")
    conta.transacoes.append(transacao)
    registrar_evento("saque", f"Conta {conta.numero} sacou R${valor:.2f}")

def transferir(origem, destino, valor):
    validar_valor(valor)
    if origem.numero == destino.numero:
        raise ValueError("Transferência para a mesma conta não é permitida.")
    if valor > origem.saldo:
        raise ValueError("Saldo insuficiente.")
    
    origem.saldo -= valor
    destino.saldo += valor

    transacao_origem = Transacao("transferência", valor, f"Transferência para {destino.numero}")
    transacao_destino = Transacao("transferência", valor, f"Transferência recebida de {origem.numero}")

    origem.transacoes.append(transacao_origem)
    destino.transacoes.append(transacao_destino)

    registrar_evento("transferência", f"{origem.numero} → {destino.numero} | R${valor:.2f}")

def extrato(conta):
    print(f"\n📄 Extrato da conta {conta.numero} ({conta.tipo})")
    for t in conta.transacoes:
        print(f"{t.data.strftime('%d/%m/%Y %H:%M')} - {t.tipo.upper()}: {t.descricao}")
    print(f"Saldo atual: R${conta.saldo:.2f}\n")
