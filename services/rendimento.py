from datetime import datetime
from models.transacao import Transacao
from utils.auditoria import registrar_evento

def aplicar_rendimento(conta, taxa_anual=0.06):
    if conta.tipo != "poupanca":
        return 0.0

    agora = datetime.now()
    dias = (agora - conta.ultimo_rendimento).days

    if dias <= 0 or conta.saldo <= 0:
        conta.ultimo_rendimento = agora
        return 0.0

    # Juros simples diário: taxa anual / 365
    taxa_diaria = taxa_anual / 365
    rendimento = conta.saldo * taxa_diaria * dias
    conta.saldo += rendimento
    conta.ultimo_rendimento = agora

    transacao = Transacao("rendimento", rendimento, f"Rendimento de {dias} dia(s)")
    conta.transacoes.append(transacao)

    registrar_evento("rendimento", f"Conta {conta.numero} recebeu R${rendimento:.2f} de rendimento")
    return rendimento
