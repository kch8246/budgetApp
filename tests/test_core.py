"""Tests for budget.core."""

from budget.core import add_transaction, get_balance


def test_add_transaction_increases_length() -> None:
    """Adding a transaction should increase the collection length by one."""
    transactions = [
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "식비",
            "description": "점심식사",
            "amount": -12000,
            "memo": "",
        }
    ]
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 2


def test_add_transaction_saves_negative_amount() -> None:
    """Negative amount transactions should be stored as expense data."""
    transactions = []
    transaction = {
        "date": "2026-01-10",
        "type": "지출",
        "category": "교통",
        "description": "지하철",
        "amount": -1500,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == -1500
    assert result[0]["type"] == "지출"


def test_add_transaction_saves_positive_amount() -> None:
    """Positive amount transactions should be stored as income data."""
    transactions = []
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == 3500000
    assert result[0]["type"] == "수입"


def test_add_transaction_handles_empty_description() -> None:
    """Empty descriptions should be preserved or normalized consistently."""
    transactions = []
    transaction = {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "",
        "amount": 25000,
        "memo": "중고마켓",
    }

    result = add_transaction(transactions, transaction)

    assert "description" in result[0]
    assert result[0]["description"] in {"", None}


def test_get_balance_returns_sum_of_income_and_expense() -> None:
    """Balance should equal total income plus total expense."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
        {
            "date": "2026-02-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4358625,
            "memo": "",
        },
        {
            "date": "2026-03-25",
            "type": "수입",
            "category": "급여",
            "description": "보너스",
            "amount": 2891172,
            "memo": "",
        },
    ]

    result = get_balance(transactions)

    assert result == 6405542


def test_get_balance_returns_zero_for_empty_list() -> None:
    """Empty transaction lists should return 0.0."""
    result = get_balance([])

    assert result == 0.0


def test_get_balance_matches_step2_csv_total() -> None:
    """Step 2 CSV-shaped data should produce the known net balance."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -65990,
            "memo": "카드결제",
        },
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
        {
            "date": "2026-02-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4358625,
            "memo": "",
        },
        {
            "date": "2026-02-13",
            "type": "수입",
            "category": "급여",
            "description": "보너스",
            "amount": 3542940,
            "memo": "",
        },
        {
            "date": "2026-03-25",
            "type": "수입",
            "category": "급여",
            "description": "보너스",
            "amount": 2891172,
            "memo": "",
        },
    ]

    result = get_balance(transactions)

    assert result == 9882492
