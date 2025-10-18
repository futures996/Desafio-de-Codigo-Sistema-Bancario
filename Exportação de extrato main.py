from services.exportacao import exportar_extrato_json, exportar_extrato_txt

# Exportar extrato em JSON
exportar_extrato_json(conta_corrente, "extrato_corrente.json")

# Exportar extrato em TXT
exportar_extrato_txt(conta_poupanca, "extrato_poupanca.txt")
