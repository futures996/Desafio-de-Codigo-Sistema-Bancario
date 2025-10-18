from services.exportacao import exportar_extrato_json, exportar_extrato_txt
from models.conta import Conta

# Simulação de contas disponíveis
contas_disponiveis = [
    Conta("0001", "corrente", saldo=1200.0),
    Conta("0002", "poupanca", saldo=5000.0)
]

def menu_exportacao():
    print("\n📤 Exportação de Extrato Bancário")
    print("Selecione a conta:")
    for i, conta in enumerate(contas_disponiveis):
        print(f"{i + 1}. Conta {conta.numero} ({conta.tipo}) - Saldo: R${conta.saldo:.2f}")

    escolha_conta = int(input("Digite o número da conta desejada: ")) - 1
    conta_selecionada = contas_disponiveis[escolha_conta]

    print("\nEscolha o formato de exportação:")
    print("1. JSON")
    print("2. TXT")
    formato = input("Digite 1 ou 2: ")

    nome_arquivo = input("Nome do arquivo (sem extensão): ")

    if formato == "1":
        exportar_extrato_json(conta_selecionada, f"{nome_arquivo}.json")
    elif formato == "2":
        exportar_extrato_txt(conta_selecionada, f"{nome_arquivo}.txt")
    else:
        print("❌ Formato inválido.")

# Executar menu
menu_exportacao()
