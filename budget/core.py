"""Core business logic for the budget CLI app."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def add_transaction(transactions: list[dict[str, Any]], transaction: dict[str, Any]) -> list[dict[str, Any]]:
    """Add a transaction to the collection and return the updated list."""
    return [*transactions, dict(transaction)]


def get_balance(transactions: list[dict[str, Any]]) -> int:
    """Return the net balance computed from the transaction list."""
    if not transactions:
        return 0.0
    return sum(int(transaction["amount"]) for transaction in transactions)


def filter_by_category(transactions: list[dict[str, Any]], category: str) -> list[dict[str, Any]]:
    """Return transactions that match the given category."""
    pass


def load_transactions_from_csv(csv_path: Path) -> list[dict[str, Any]]:
    """Load transactions from a CSV file and return them as dictionaries."""
    pass


def monthly_summary(transactions: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Summarize transactions by month."""
    pass
