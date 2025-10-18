class Cliente:
    def __init__(self, nome, cpf, senha_hash):
        self.nome = nome
        self.cpf = cpf
        self.senha_hash = senha_hash
        self.contas = []
