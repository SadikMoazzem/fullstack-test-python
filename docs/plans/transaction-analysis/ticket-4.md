# Ticket 4: Add tests for get_income_summary

**File:** `test_main.py`

Add tests for the `get_income_summary` function (TDD red phase).

**Actions:**

1. Import `get_income_summary` and `Summary` from main
2. Create `TestGetIncomeSummary` class
3. Add test using the existing `transactions` fixture
4. Add test for empty transaction list
5. Add test for list with no income (all spending)

**Example:**

```python
from decimal import Decimal

from main import get_income_summary, Summary


class TestGetIncomeSummary:
    def test_returns_correct_count_and_total(self, transactions: list[dict[str, str]]) -> None:
        result = get_income_summary(transactions)
        assert isinstance(result, Summary)
        assert result.count == 5
        assert result.total == Decimal("5023.95")

    def test_empty_list_returns_zero(self) -> None:
        result = get_income_summary([])
        assert result.count == 0
        assert result.total == Decimal("0")

    def test_all_spending_returns_zero(self) -> None:
        spending_only = [{"amount": "-100.00"}, {"amount": "-50.00"}]
        result = get_income_summary(spending_only)
        assert result.count == 0
        assert result.total == Decimal("0")
```

**Checks:**

- Tests exist and can be discovered by pytest
- Tests fail with ImportError or AssertionError (TDD red phase)
