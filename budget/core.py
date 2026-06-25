"""Core business logic for the budget CLI app."""

from __future__ import annotations

import csv
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
    normalized_category = category.lower()
    return [transaction for transaction in transactions if str(transaction["category"]).lower() == normalized_category]


def load_transactions_from_csv(csv_path: Path) -> list[dict[str, Any]]:
    """Load transactions from a CSV file and return them as dictionaries."""
    with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            {
                "date": row["date"],
                "type": row["type"],
                "category": row["category"],
                "description": row["description"],
                "amount": int(row["amount"]),
                "memo": row["memo"],
            }
            for row in reader
        ]


def monthly_summary(transactions: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Summarize transactions by month."""
    summary: dict[str, dict[str, int]] = {}

    for transaction in transactions:
        month = str(transaction["date"])[:7]
        amount = int(transaction["amount"])
        month_summary = summary.setdefault(month, {"income": 0, "expense": 0, "net": 0})
        if amount >= 0:
            month_summary["income"] += amount
        else:
            month_summary["expense"] += amount
        month_summary["net"] += amount

    return summary
