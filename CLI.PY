from services import BankService
from storage import Storage
from models import AccountType


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Valor não pode ser vazio.")


def input_float(prompt: str) -> float:
    while True:
        try:
            v = float(input(prompt).replace(",", "."))
            return v
        except ValueError:
            print("Informe um número válido.")


class CLI:
    def __init__(self):
        self.storage = Storage()
        self.bank = BankService(self.storage)
        self.current_customer = None

    def run(self):
        while True:
            self._print_header()
            print("1. Entrar")
            print("2. Cadastrar cliente")
            print("3. Sair")
            choice = input("Escolha: ").strip()
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                print("Até logo!")
                break
            else:
                print("Opção inválida.")

    def _print_header(self):
        print("\n=== Banco Minas ===")

    def login(self):
        cpf = input_non_empty("CPF: ")
        password = input_non_empty("Senha: ")
        customer = self.bank.authenticate(cpf, password)
        if not customer:
            print("Credenciais inválidas.")
            return
        self.current_customer = customer
        self.dashboard()

    def register(self):
        name = input_non_empty("Nome: ")
        cpf = input_non_empty("CPF: ")
        email = input_non_empty("Email: ")
        password = input_non_empty("Senha: ")
        try:
            customer = self.bank.create_customer(name, cpf, email, password)
            print(f"Cliente criado: {customer.name} (ID: {customer.id})")
            acc = self.bank.create_account(customer.id, AccountType.CORRENTE)
            print(f"Conta criada: {acc.number} - Tipo: {acc.type.value}")
        except ValueError as e:
            print(f"Erro: {e}")

    def dashboard(self):
        while True:
            print(f"\nBem-vindo(a), {self.current_customer.name}")
            print("Contas:", ", ".join(self.current_customer.accounts) or "Nenhuma")
            print("1. Criar conta")
            print("2. Depositar")
            print("3. Sacar")
            print("4. Transferir")
            print("5. Extrato")
            print("6. Trocar usuário")
            print("7. Sair")
            choice = input("Escolha: ").strip()

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                self.statement()
            elif choice == "6":
                self.current_customer = None
                break
            elif choice == "7":
                exit(0)
            else:
                print("Opção inválida.")

    def create_account(self):
        print("Tipos: 1-Corrente  2-Poupança")
        t = input("Tipo: ").strip()
        t = AccountType.CORRENTE if t == "1" else AccountType.POUPANCA
        try:
            acc = self.bank.create_account(self.current_customer.id, t)
            self.current_customer = self.bank.storage.get_customer_by_id(self.current_customer.id)
            print(f"Conta criada: {acc.number} ({acc.type.value})")
        except ValueError as e:
            print(f"Erro: {e}")

    def _pick_account(self, prompt="Número da conta: "):
        if not self.current_customer.accounts:
            print("Você não possui contas.")
            return None
        print("Suas contas:", ", ".join(self.current_customer.accounts))
        acc = input_non_empty(prompt)
        if acc not in self.current_customer.accounts:
            print("Conta não pertence ao usuário.")
            return None
        return acc

    def deposit(self):
        acc = self._pick_account()
        if not acc:
            return
        amount = input_float("Valor do depósito: ")
        try:
            balance = self.bank.deposit(acc, amount)
            print(f"Depósito realizado. Saldo: R$ {balance:.2f}")
        except ValueError as e:
            print(f"Erro: {e}")

    def withdraw(self):
        acc = self._pick_account()
        if not acc:
            return
        amount = input_float("Valor do saque: ")
        try:
            balance = self.bank.withdraw(acc, amount)
            print(f"Saque realizado. Saldo: R$ {balance:.2f}")
        except ValueError as e:
            print(f"Erro: {e}")

    def transfer(self):
        src = self._pick_account("Conta origem: ")
        if not src:
            return
        dst = input_non_empty("Conta destino (ex: 0001-12345678): ")
        amount = input_float("Valor da transferência: ")
        try:
            src_balance, dst_balance = self.bank.transfer(src, dst, amount)
            print(f"Transferência ok. Saldo origem: R$ {src_balance:.2f}")
        except ValueError as e:
            print(f"Erro: {e}")

    def statement(self):
        acc = self._pick_account()
        if not acc:
            return
        try:
            account = self.bank.statement(acc)
            print(f"\nExtrato da conta {account.number} - Saldo: R$ {account.balance:.2f}")
            print("-" * 40)
            for t in account.transactions[-50:]:  # últimos 50 lançamentos
                print(f"{t.timestamp} | {t.description:22} | {t.amount:8.2f} | Saldo: {t.balance_after:8.2f}")
            print("-" * 40)
        except ValueError as e:
            print(f"Erro: {e}")
