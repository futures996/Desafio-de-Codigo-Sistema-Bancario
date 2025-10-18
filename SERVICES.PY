from typing import Optional, Tuple
from models import Customer, Account, AccountType
from storage import Storage
import uuid
import hashlib
import re


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def validate_cpf(cpf: str) -> bool:
    # Validação simplificada (formato e dígitos). Para produção, aplique regras completas.
    clean = re.sub(r"\D", "", cpf)
    return len(clean) == 11


class BankService:
    def __init__(self, storage: Storage):
        self.storage = storage

    # Autenticação
    def authenticate(self, cpf: str, password: str) -> Optional[Customer]:
        customer = self.storage.get_customer_by_cpf(cpf)
        if not customer:
            return None
        if customer.password_hash != hash_password(password):
            return None
        return customer

    # Clientes
    def create_customer(self, name: str, cpf: str, email: str, password: str) -> Customer:
        if not validate_cpf(cpf):
            raise ValueError("CPF inválido.")
        if self.storage.get_customer_by_cpf(cpf):
            raise ValueError("CPF já cadastrado.")
        cid = str(uuid.uuid4())
        customer = Customer(
            id=cid,
            name=name.strip(),
            cpf=re.sub(r"\D", "", cpf),
            email=email.strip(),
            password_hash=hash_password(password),
        )
        self.storage.upsert_customer(customer)
        return customer

    # Contas
    def create_account(self, customer_id: str, type: AccountType = AccountType.CORRENTE) -> Account:
        customer = self.storage.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError("Cliente não encontrado.")
        number = self._generate_account_number()
        account = Account(number=number, customer_id=customer.id, type=type)
        self.storage.upsert_account(account)
        customer.add_account(account.number)
        self.storage.upsert_customer(customer)
        return account

    def _generate_account_number(self) -> str:
        # Número: agência fixa 0001 + 8 dígitos pseudo-únicos
        base = str(uuid.uuid4().int)[-8:]
        return f"0001-{base}"

    # Operações
    def deposit(self, account_number: str, amount: float) -> float:
        account = self.storage.get_account_by_number(account_number)
        if not account:
            raise ValueError("Conta não encontrada.")
        account.deposit(amount)
        self.storage.upsert_account(account)
        return account.balance

    def withdraw(self, account_number: str, amount: float) -> float:
        account = self.storage.get_account_by_number(account_number)
        if not account:
            raise ValueError("Conta não encontrada.")
        account.withdraw(amount)
        self.storage.upsert_account(account)
        return account.balance

    def transfer(self, source_number: str, target_number: str, amount: float) -> Tuple[float, float]:
        source = self.storage.get_account_by_number(source_number)
        target = self.storage.get_account_by_number(target_number)
        if not source or not target:
            raise ValueError("Conta origem ou destino não encontrada.")
        source.transfer_to(target, amount)
        self.storage.upsert_account(source)
        self.storage.upsert_account(target)
        return source.balance, target.balance

    def statement(self, account_number: str):
        account = self.storage.get_account_by_number(account_number)
        if not account:
            raise ValueError("Conta não encontrada.")
        return account
