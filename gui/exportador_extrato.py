import tkinter as tk
from tkinter import ttk, messagebox
from services.exportacao import exportar_extrato_json, exportar_extrato_txt
from models.conta import Conta

# Simulação de contas disponíveis
contas_disponiveis = [
    Conta("0001", "corrente", saldo=1200.0),
    Conta("0002", "poupanca", saldo=5000.0)
]

def exportar():
    conta_index = combo_contas.current()
    formato = formato_var.get()
    nome_arquivo = entrada_nome.get()

    if conta_index == -1 or not nome_arquivo:
        messagebox.showerror("Erro", "Selecione uma conta e informe o nome do arquivo.")
        return

    conta = contas_disponiveis[conta_index]

    try:
        if formato == "JSON":
            exportar_extrato_json(conta, f"{nome_arquivo}.json")
        else:
            exportar_extrato_txt(conta, f"{nome_arquivo}.txt")
        messagebox.showinfo("Sucesso", f"Extrato exportado como {formato}.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Interface
janela = tk.Tk()
janela.title("Exportador de Extrato Bancário")
janela.geometry("400x250")

ttk.Label(janela, text="Selecione a conta:").pack(pady=5)
combo_contas = ttk.Combobox(janela, values=[
    f"{c.numero} ({c.tipo}) - R${c.saldo:.2f}" for c in contas_disponiveis
])
combo_contas.pack()

ttk.Label(janela, text="Formato de exportação:").pack(pady=5)
formato_var = tk.StringVar(value="JSON")
ttk.Radiobutton(janela, text="JSON", variable=formato_var, value="JSON").pack()
ttk.Radiobutton(janela, text="TXT", variable=formato_var, value="TXT").pack()

ttk.Label(janela, text="Nome do arquivo:").pack(pady=5)
entrada_nome = ttk.Entry(janela)
entrada_nome.pack()

ttk.Button(janela, text="Exportar Extrato", command=exportar).pack(pady=15)

janela.mainloop()
