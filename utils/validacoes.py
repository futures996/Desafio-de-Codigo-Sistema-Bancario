def validar_valor(valor):
    if valor <= 0:
        raise ValueError("Valor deve ser positivo.")
