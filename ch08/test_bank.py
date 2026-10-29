# test_bank.py
import pytest
from bank import apply_transaction, process, InsufficientFunds

def test_deposit():
    assert apply_transaction(100, "deposit", 50) == 150

def test_overdraft_rejected():
    with pytest.raises(InsufficientFunds):
        apply_transaction(100, "withdraw", 500)

def test_process_collects_failures():
    final, failures = process(100, [("deposit", 50), ("withdraw", 999), ("refund", 5)])
    assert final == 150
    assert len(failures) == 2
