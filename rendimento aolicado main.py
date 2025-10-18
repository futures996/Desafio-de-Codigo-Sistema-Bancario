from services.rendimento import aplicar_rendimento

# Simular que passaram 10 dias
conta_poupanca.ultimo_rendimento -= timedelta(days=10)

rendimento = aplicar_rendimento(conta_poupanca)
print(f"Rendimento aplicado: R$ {rendimento:.2f}")
