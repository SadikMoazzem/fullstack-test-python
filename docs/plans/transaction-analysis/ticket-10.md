# Ticket 10: Add tests for get_salary_by_payer

**File:** `test_main.py`

Add tests for the `get_salary_by_payer` function (TDD red phase).

**Actions:**

1. Import `get_salary_by_payer` and `PayerSummary` from main
2. Create `TestGetSalaryByPayer` class
3. Add test using the existing `transactions` fixture
4. Add test for empty transaction list
5. Add test for transactions with no salary category
6. Verify payer is extracted from description field

**Example:**

```python
from decimal import Decimal

from main import get_salary_by_payer, PayerSummary


class TestGetSalaryByPayer:
    def test_returns_correct_breakdown(self, transactions: list[dict[str, str]]) -> None:
        result = get_salary_by_payer(transactions)
        assert all(isinstance(r, PayerSummary) for r in result)

        # Should have one payer: WEB GENIUS
        assert len(result) == 1
        assert result[0].payer == "WEB GENIUS"
        assert result[0].count == 3
        assert result[0].total == Decimal("4700.00")

    def test_empty_list_returns_empty(self) -> None:
        result = get_salary_by_payer([])
        assert result == []

    def test_no_salary_transactions_returns_empty(self) -> None:
        non_salary = [
            {"amount": "100.00", "category": "Benefits", "description": "REBATE"},
            {"amount": "-50.00", "category": "Shopping", "description": "STORE"},
        ]
        result = get_salary_by_payer(non_salary)
        assert result == []

    def test_multiple_payers(self) -> None:
        multi_payer = [
            {"amount": "1000.00", "category": "Salary", "description": "COMPANY A"},
            {"amount": "500.00", "category": "Salary", "description": "COMPANY B"},
            {"amount": "1000.00", "category": "Salary", "description": "COMPANY A"},
        ]
        result = get_salary_by_payer(multi_payer)
        by_payer = {r.payer: r for r in result}

        assert by_payer["COMPANY A"].count == 2
        assert by_payer["COMPANY A"].total == Decimal("2000.00")
        assert by_payer["COMPANY B"].count == 1
        assert by_payer["COMPANY B"].total == Decimal("500.00")
```

**Checks:**

- Tests exist and can be discovered by pytest
- Tests fail with ImportError or AssertionError (TDD red phase)
