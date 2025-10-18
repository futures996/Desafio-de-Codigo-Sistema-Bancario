from datetime import datetime

class Transacao:
    def __init__(self, tipo, valor, descricao):
        self.tipo = tipo
        self.valor = valor
        self.descricao = descricao
        self.data = datetime.now()
