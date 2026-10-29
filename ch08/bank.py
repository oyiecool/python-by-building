# bank.py
import logging
log = logging.getLogger(__name__)

class InsufficientFunds(Exception):
    pass

def apply_transaction(balance: float, kind: str, amount: float) -> float:
    if amount <= 0:
        raise ValueError("amount must be positive")
    if kind == "deposit":
        new = balance + amount
    elif kind == "withdraw":
        if amount > balance:
            raise InsufficientFunds(f"balance {balance:.2f} < {amount:.2f}")
        new = balance - amount
    else:
        raise ValueError(f"unknown transaction type {kind!r}")
    log.info("%s %.2f -> balance %.2f", kind, amount, new)
    return round(new, 2)

def process(balance: float, transactions: list[tuple[str, float]]) -> tuple[float, list[str]]:
    """Apply all transactions; collect failures instead of stopping."""
    failures = []
    for kind, amount in transactions:
        try:
            balance = apply_transaction(balance, kind, amount)
        except (ValueError, InsufficientFunds) as e:
            failures.append(f"{kind} {amount}: {e}")
    return balance, failures
