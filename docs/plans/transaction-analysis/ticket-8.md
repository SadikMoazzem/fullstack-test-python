# Ticket 8: Add tests for get_spending_by_category

**File:** `test_main.py`

Add tests for the `get_spending_by_category` function (TDD red phase).

**Actions:**

1. Import `get_spending_by_category` and `CategorySummary` from main
2. Create `TestGetSpendingByCategory` class
3. Add test using the existing `transactions` fixture
4. Add test for empty transaction list
5. Add test for transactions with empty category (should be "Uncategorized")
6. Verify correct categories: Shopping, Bills and Utilities, Food & Dining, Uncategorized

**Example:**

```python
from decimal import Decimal

from main import get_spending_by_category, CategorySummary


class TestGetSpendingByCategory:
    def test_returns_correct_breakdown(self, transactions: list[dict[str, str]]) -> None:
        result = get_spending_by_category(transactions)
        assert all(isinstance(r, CategorySummary) for r in result)

        # Convert to dict for easier assertion
        by_category = {r.category: r for r in result}

        assert by_category["Shopping"].count == 5
        assert by_category["Shopping"].total == Decimal("-136.30")

        assert by_category["Bills and Utilities"].count == 2
        assert by_category["Bills and Utilities"].total == Decimal("-69.86")

        assert by_category["Food & Dining"].count == 1
        assert by_category["Food & Dining"].total == Decimal("-17.40")

    def test_empty_category_becomes_uncategorized(self, transactions: list[dict[str, str]]) -> None:
        result = get_spending_by_category(transactions)
        by_category = {r.category: r for r in result}

        # 3 spending transactions have no category
        assert "Uncategorized" in by_category
        assert by_category["Uncategorized"].count == 3
        assert by_category["Uncategorized"].total == Decimal("-101.75")

    def test_empty_list_returns_empty(self) -> None:
        result = get_spending_by_category([])
        assert result == []
```

**Checks:**

- Tests exist and can be discovered by pytest
- Tests fail with ImportError or AssertionError (TDD red phase)
