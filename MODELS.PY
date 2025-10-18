from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum
import uuid


class AccountType(str, Enum):
    CORRENTE = "CORRENTE"
    POUPANCA = "POUPANCA"


@dataclass
class Transaction:
    id: str
    timestamp: str
    description: str
    amount: float
    balance_after: float
    source_account: Optional[str] = None
    target_account: Optional[str] = None

    @staticmethod
    def create(description: str, amount: float, balance_after: float,
               source_account: Optional[str] = None,
               target_account: Optional[str] = None) -> "Transaction":
        return Transaction(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(timespec="seconds"),
            description=description,
            amount=amount,
            balance_after=balance_after,
            source_account=source_account,
            target_account=target_account
        )


@dataclass
class Account:
    number: str
    customer_id: str
    type: AccountType
    balance: float = 0.0
    transactions: List[Transaction] = field(default_factory=list)
    daily_withdraw_limit: float = 1000.0
    per_withdraw_limit: float = 600.0

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Valor do depósito deve ser positivo.")
        self.balance += amount
        self.transactions.append(Transaction.create(
            description="Depósito",
            amount=amount,
            balance_after=self.balance
        ))

    def can_withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Valor do saque deve ser positivo.")
        if amount > self.per_withdraw_limit:
            raise ValueError(f"Saque acima do limite por operação ({self.per_withdraw_limit:.2f}).")
        if amount > self.balance:
            raise ValueError("Saldo insuficiente.")

    def withdraw(self, amount: float):
        self.can_withdraw(amount)
        self.balance -= amount
        self.transactions.append(Transaction.create(
            description="Saque",
            amount=-amount,
            balance_after=self.balance
        ))

    def transfer_to(self, target: "Account", amount: float):
        if self.number == target.number:
            raise ValueError("Não é possível transferir para a mesma conta.")
        self.can_withdraw(amount)
        target.balance += amount
        self.balance -= amount
        txn_out = Transaction.create(
            description="Transferência enviada",
            amount=-amount,
            balance_after=self.balance,
            source_account=self.number,
            target_account=target.number
        )
        txn_in = Transaction.create(
            description="Transferência recebida",
            amount=amount,
            balance_after=target.balance,
            source_account=self.number,
            target_account=target.number
        )
        self.transactions.append(txn_out)
        target.transactions.append(txn_in)


@dataclass
class Customer:
    id: str
    name: str
    cpf: str
    email: str
    password_hash: str
    accounts: List[str] = field(default_factory=list)

    def add_account(self, account_number: str):
        if account_number not in self.accounts:
            self.accounts.append(account_number)
