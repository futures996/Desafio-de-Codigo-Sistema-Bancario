from datetime import datetime

def registrar_evento(tipo, mensagem):
    print(f"[{datetime.now()}] {tipo.upper()}: {mensagem}")
