import json

def exportar_extrato_json(conta, caminho_arquivo):
    dados = {
        "numero_conta": conta.numero,
        "tipo": conta.tipo,
        "saldo": conta.saldo,
        "transacoes": [
            {
                "data": t.data.strftime("%Y-%m-%d %H:%M:%S"),
                "tipo": t.tipo,
                "valor": t.valor,
                "descricao": t.descricao
            }
            for t in conta.transacoes
        ]
    }
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print(f"✅ Extrato exportado para {caminho_arquivo} (JSON)")

def exportar_extrato_txt(conta, caminho_arquivo):
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(f"Extrato da conta {conta.numero} ({conta.tipo})\n")
        f.write(f"Saldo atual: R$ {conta.saldo:.2f}\n\n")
        for t in conta.transacoes:
            linha = f"{t.data.strftime('%d/%m/%Y %H:%M')} - {t.tipo.upper()}: {t.descricao} (R$ {t.valor:.2f})\n"
            f.write(linha)
    print(f"✅ Extrato exportado para {caminho_arquivo} (TXT)")
