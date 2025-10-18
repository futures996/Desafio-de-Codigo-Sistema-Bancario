import json
import os
from typing import Dict, Any, Optional, List
from models import Customer, Account, Transaction, AccountType


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "bank_data.json")


def serialize_customer(c: Customer) -> Dict[str, Any]:
    return {
        "id": c.id,
        "name": c.name,
        "cpf": c.cpf,
        "email": c.email,
        "password_hash": c.password_hash,
        "accounts": c.accounts,
    }


def deserialize_customer(d: Dict[str, Any]) -> Customer:
    return Customer(
        id=d["id"],
        name=d["name"],
        cpf=d["cpf"],
        email=d["email"],
        password_hash=d["password_hash"],
        accounts=d.get("accounts", [])
    )


def serialize_account(a: Account) -> Dict[str, Any]:
    return {
        "number": a.number,
        "customer_id": a.customer_id,
        "type": a.type.value,
        "balance": a.balance,
        "transactions": [serialize_transaction(t) for t in a.transactions],
        "daily_withdraw_limit": a.daily_withdraw_limit,
        "per_withdraw_limit": a.per_withdraw_limit
    }


def deserialize_account(d: Dict[str, Any]) -> Account:
    acc = Account(
        number=d["number"],
        customer_id=d["customer_id"],
        type=AccountType(d["type"]),
        balance=d.get("balance", 0.0),
        transactions=[deserialize_transaction(t) for t in d.get("transactions", [])],
        daily_withdraw_limit=d.get("daily_withdraw_limit", 1000.0),
        per_withdraw_limit=d.get("per_withdraw_limit", 600.0)
    )
    return acc


def serialize_transaction(t: Transaction) -> Dict[str, Any]:
    return {
        "id": t.id,
        "timestamp": t.timestamp,
        "description": t.description,
        "amount": t.amount,
        "balance_after": t.balance_after,
        "source_account": t.source_account,
        "target_account": t.target_account
    }


def deserialize_transaction(d: Dict[str, Any]) -> Transaction:
    return Transaction(
        id=d["id"],
        timestamp=d["timestamp"],
        description=d["description"],
        amount=d["amount"],
        balance_after=d["balance_after"],
        source_account=d.get("source_account"),
        target_account=d.get("target_account")
    )


class Storage:
    def __init__(self, path: Optional[str] = None):
        self.path = path or DEFAULT_PATH
        self.data: Dict[str, Any] = {"customers": [], "accounts": []}
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.path):
            self._save()
        else:
            self._load()

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = {"customers": [], "accounts": []}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def list_customers(self) -> List[Customer]:
        return [deserialize_customer(c) for c in self.data.get("customers", [])]

    def list_accounts(self) -> List[Account]:
        return [deserialize_account(a) for a in self.data.get("accounts", [])]

    def get_customer_by_cpf(self, cpf: str) -> Optional[Customer]:
        for c in self.list_customers():
            if c.cpf == cpf:
                return c
        return None

    def get_customer_by_id(self, cid: str) -> Optional[Customer]:
        for c in self.list_customers():
            if c.id == cid:
                return c
        return None

    def get_account_by_number(self, number: str) -> Optional[Account]:
        for a in self.list_accounts():
            if a.number == number:
                return a
        return None

    def upsert_customer(self, c: Customer):
        customers = self.list_customers()
        found = False
        for i, cust in enumerate(customers):
            if cust.id == c.id:
                customers[i] = c
                found = True
                break
        if not found:
            customers.append(c)
        self.data["customers"] = [serialize_customer(x) for x in customers]
        self._save()

    def upsert_account(self, a: Account):
        accounts = self.list_accounts()
        found = False
        for i, acc in enumerate(accounts):
            if acc.number == a.number:
                accounts[i] = a
                found = True
                break
        if not found:
            accounts.append(a)
        self.data["accounts"] = [serialize_account(x) for x in accounts]
        self._save()
