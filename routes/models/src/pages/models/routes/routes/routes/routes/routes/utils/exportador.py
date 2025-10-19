import csv
from fpdf import FPDF

def exportar_csv(transacoes, caminho):
    with open(caminho, mode="w", newline="") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["ID", "Tipo", "Valor", "Origem", "Destino"])
        for t in transacoes:
            writer.writerow([t.id, t.tipo, t.valor, t.conta_origem, t.conta_destino])

def exportar_pdf(transacoes, caminho):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Extrato Bancário", ln=True, align="C")
    for t in transacoes:
        linha = f"{t.id} | {t.tipo} | R${t.valor:.2f} | {t.conta_origem} -> {t.conta_destino or '-'}"
        pdf.cell(200, 10, txt=linha, ln=True)
    pdf.output(caminho)
