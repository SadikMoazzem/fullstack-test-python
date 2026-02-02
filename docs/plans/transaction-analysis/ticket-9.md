# Ticket 9: Implement get_spending_by_category

**File:** `main.py`

Implement the `get_spending_by_category` function to make tests pass.

**Actions:**

1. Add `get_spending_by_category(transactions: list[dict[str, str]]) -> list[CategorySummary]` function
2. Filter to only spending transactions (amount < 0)
3. Group by category (use "Uncategorized" for empty category)
4. For each category, calculate count and total
5. Return list of CategorySummary instances

**Example:**

```python
def get_spending_by_category(transactions: list[dict[str, str]]) -> list[CategorySummary]:
    """Break down spending by category."""
    categories: dict[str, list[Decimal]] = {}

    for t in transactions:
        amount = Decimal(t["amount"])
        if amount >= 0:
            continue

        category = t.get("category", "") or "Uncategorized"
        if category not in categories:
            categories[category] = []
        categories[category].append(amount)

    return [
        CategorySummary(
            category=cat,
            count=len(amounts),
            total=sum(amounts, Decimal("0"))
        )
        for cat, amounts in sorted(categories.items())
    ]
```

**Checks:**

- Run `poetry run pytest test_main.py::TestGetSpendingByCategory -v`
- All tests pass
