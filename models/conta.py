class Conta:
    def __init__(self, numero, tipo, saldo=0.0):
        self.numero = numero
        self.tipo = tipo  # 'corrente' ou 'poupanca'
        self.saldo = saldo
        self.transacoes = []
