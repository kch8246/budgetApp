"""Tests for budget.core."""

from budget.core import add_transaction


def test_add_transaction_increases_length() -> None:
    """Adding a transaction should increase the collection length by one."""
    transactions = [{"amount": 1000}]
    transaction = {"amount": 500}

    result = add_transaction(transactions, transaction)

    assert len(result) == 2

