# Ticket 6: Add tests for get_spending_summary

**File:** `test_main.py`

Add tests for the `get_spending_summary` function (TDD red phase).

**Actions:**

1. Import `get_spending_summary` from main
2. Create `TestGetSpendingSummary` class
3. Add test using the existing `transactions` fixture
4. Add test for empty transaction list
5. Add test for list with no spending (all income)

**Example:**

```python
from decimal import Decimal

from main import get_spending_summary, Summary


class TestGetSpendingSummary:
    def test_returns_correct_count_and_total(self, transactions: list[dict[str, str]]) -> None:
        result = get_spending_summary(transactions)
        assert isinstance(result, Summary)
        assert result.count == 11
        assert result.total == Decimal("-325.31")

    def test_empty_list_returns_zero(self) -> None:
        result = get_spending_summary([])
        assert result.count == 0
        assert result.total == Decimal("0")

    def test_all_income_returns_zero(self) -> None:
        income_only = [{"amount": "100.00"}, {"amount": "50.00"}]
        result = get_spending_summary(income_only)
        assert result.count == 0
        assert result.total == Decimal("0")
```

**Checks:**

- Tests exist and can be discovered by pytest
- Tests fail with ImportError or AssertionError (TDD red phase)
