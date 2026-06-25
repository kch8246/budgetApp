"""Tests for budget.core."""

from pathlib import Path

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    load_transactions_from_csv,
    monthly_summary,
)


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


def test_filter_by_category_matches_real_category_case_insensitively() -> None:
    """Filtering should match real CSV categories regardless of case."""
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
            "date": "2026-01-14",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -282323,
            "memo": "메모_1",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -65990,
            "memo": "카드결제",
        },
    ]

    result = filter_by_category(transactions, "여행")

    assert len(result) == 2
    assert all(transaction["category"] == "여행" for transaction in result)


def test_filter_by_category_returns_empty_list_for_missing_category() -> None:
    """Unknown categories should return an empty list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        }
    ]

    result = filter_by_category(transactions, "없는카테고리")

    assert result == []


def test_filter_by_category_returns_independent_result_list() -> None:
    """Mutating filtered results should not change the original list."""
    transactions = [
        {
            "date": "2026-02-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4358625,
            "memo": "",
        }
    ]

    result = filter_by_category(transactions, "급여")
    result.append(
        {
            "date": "2026-02-02",
            "type": "수입",
            "category": "급여",
            "description": "추가",
            "amount": 1,
            "memo": "",
        }
    )

    assert len(transactions) == 1
    assert len(result) == 2


def test_load_transactions_from_csv_reads_step1_data() -> None:
    """CSV loading should parse step1 transactions into dictionaries."""
    result = load_transactions_from_csv(Path("data/step1_transactions.csv"))

    assert len(result) == 10
    assert result[0]["date"] == "2026-01-05"
    assert result[0]["type"] == "지출"
    assert result[0]["category"] == "식비"
    assert result[0]["description"] == "점심식사"
    assert result[0]["amount"] == -12000
    assert isinstance(result[0]["amount"], int)
    assert result[1]["amount"] == 3500000
    assert result[9]["memo"] == "중고마켓"


def test_monthly_summary_groups_income_expense_and_net() -> None:
    """Monthly summary should aggregate income, expense, and net by month."""
    transactions = [
        {
            "date": "2025-01-02",
            "type": "지출",
            "category": "저축/투자",
            "description": "펀드 투자",
            "amount": -542738,
            "memo": "",
        },
        {
            "date": "2025-01-04",
            "type": "수입",
            "category": "기타수입",
            "description": "환급금",
            "amount": 405037,
            "memo": "메모_53",
        },
        {
            "date": "2025-01-31",
            "type": "지출",
            "category": "여행",
            "description": "숙박비",
            "amount": -1277935,
            "memo": "현금",
        },
        {
            "date": "2025-02-11",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4995758,
            "memo": "현금",
        },
        {
            "date": "2025-02-24",
            "type": "수입",
            "category": "기타수입",
            "description": "환급금",
            "amount": 256099,
            "memo": "메모_90",
        },
        {
            "date": "2025-02-24",
            "type": "지출",
            "category": "문화/여가",
            "description": "스포츠센터",
            "amount": -40697,
            "memo": "카드결제",
        },
    ]

    result = monthly_summary(transactions)

    assert result == {
        "2025-01": {"income": 405037, "expense": -1820673, "net": -1415636},
        "2025-02": {"income": 5251857, "expense": -40697, "net": 5211160},
    }


def test_monthly_summary_matches_step3_january_and_march_totals() -> None:
    """Step 3 data should produce known month totals."""
    transactions = load_transactions_from_csv(Path("data/step3_transactions.csv"))

    result = monthly_summary(transactions)

    assert result["2025-01"] == {"income": 405037, "expense": -2886860, "net": -2481823}
    assert result["2025-03"] == {"income": 54659, "expense": -5602558, "net": -5547899}
