import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from services.exportacao import exportar_extrato_json, exportar_extrato_txt
from services.rendimento import aplicar_rendimento
from models.conta import Conta

# Simulação de contas
contas_disponiveis = [
    Conta("0001", "corrente", saldo=1200.0),
    Conta("0002", "poupanca", saldo=5000.0)
]

# Simular transações
contas_disponiveis[0].depositar(300)
contas_disponiveis[0].sacar(100)
contas_disponiveis[1].depositar(1000)
contas_disponiveis[1].sacar(200)

def atualizar_dashboard():
    conta = contas_disponiveis[combo_contas.current()]
    saldo_var.set(f"R$ {conta.saldo:.2f}")
    rendimento = aplicar_rendimento(conta)
    rendimento_var.set(f"R$ {rendimento:.2f}")
    atualizar_extrato()

def atualizar_extrato():
    conta = contas_disponiveis[combo_contas.current()]
    tipo_filtro = tipo_var.get()
    data_inicio = entrada_inicio.get()
    data_fim = entrada_fim.get()

    extrato_box.delete(1.0, tk.END)
    for t in conta.transacoes:
        if tipo_filtro != "Todos" and t.tipo != tipo_filtro:
            continue
        if data_inicio:
            inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
            if t.data < inicio:
                continue
        if data_fim:
            fim = datetime.strptime(data_fim, "%d/%m/%Y")
            if t.data > fim:
                continue
        linha = f"{t.data.strftime('%d/%m/%Y %H:%M')} - {t.tipo.upper()}: {t.descricao} (R$ {t.valor:.2f})\n"
        extrato_box.insert(tk.END, linha)

def exportar():
    conta = contas_disponiveis[combo_contas.current()]
    nome_arquivo = entrada_nome.get()
    formato = formato_var.get()
    if not nome_arquivo:
        messagebox.showerror("Erro", "Informe o nome do arquivo.")
        return
    if formato == "JSON":
        exportar_extrato_json(conta, f"{nome_arquivo}.json")
    else:
        exportar_extrato_txt(conta, f"{nome_arquivo}.txt")
    messagebox.showinfo("Sucesso", f"Extrato exportado como {formato}.")

# Interface
janela = tk.Tk()
janela.title("Dashboard Bancário")
janela.geometry("600x600")

ttk.Label(janela, text="Selecione a conta:").pack()
combo_contas = ttk.Combobox(janela, values=[
    f"{c.numero} ({c.tipo}) - R${c.saldo:.2f}" for c in contas_disponiveis
])
combo_contas.pack()
combo_contas.current(0)

ttk.Button(janela, text="Atualizar Dashboard", command=atualizar_dashboard).pack(pady=5)

saldo_var = tk.StringVar()
rendimento_var = tk.StringVar()
ttk.Label(janela, text="Saldo atual:").pack()
ttk.Label(janela, textvariable=saldo_var).pack()
ttk.Label(janela, text="Rendimento aplicado:").pack()
ttk.Label(janela, textvariable=rendimento_var).pack()

ttk.Label(janela, text="Filtrar por tipo:").pack()
tipo_var = tk.StringVar(value="Todos")
ttk.Combobox(janela, textvariable=tipo_var, values=["Todos", "depósito", "saque", "transferência", "rendimento"]).pack()

ttk.Label(janela, text="Data início (dd/mm/aaaa):").pack()
entrada_inicio = ttk.Entry(janela)
entrada_inicio.pack()

ttk.Label(janela, text="Data fim (dd/mm/aaaa):").pack()
entrada_fim = ttk.Entry(janela)
entrada_fim.pack()

ttk.Button(janela, text="Filtrar Extrato", command=atualizar_extrato).pack(pady=5)

extrato_box = tk.Text(janela, height=15, width=70)
extrato_box.pack()

ttk.Label(janela, text="Nome do arquivo para exportar:").pack()
entrada_nome = ttk.Entry(janela)
entrada_nome.pack()

formato_var = tk.StringVar(value="JSON")
ttk.Radiobutton(janela, text="JSON", variable=formato_var, value="JSON").pack()
ttk.Radiobutton(janela, text="TXT", variable=formato_var, value="TXT").pack()

ttk.Button(janela, text="Exportar Extrato", command=exportar).pack(pady=10)

janela.mainloop()
