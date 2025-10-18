from services.operacoes import depositar, sacar, transferir, extrato

# Depósito
depositar(conta, 500)

# Saque
sacar(conta, 200)

# Transferência
transferir(conta_corrente, conta_poupanca, 300)

# Extrato
extrato(conta_corrente)
