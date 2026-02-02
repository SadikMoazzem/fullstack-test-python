# Ticket 7: Implement get_spending_summary

**File:** `main.py`

Implement the `get_spending_summary` function to make tests pass.

**Actions:**

1. Add `get_spending_summary(transactions: list[dict[str, str]]) -> Summary` function
2. Filter transactions where amount < 0
3. Count and sum the filtered transactions
4. Return a Summary dataclass instance

**Example:**

```python
def get_spending_summary(transactions: list[dict[str, str]]) -> Summary:
    """Calculate total spending (negative amounts) count and sum."""
    spending_transactions = [
        Decimal(t["amount"])
        for t in transactions
        if Decimal(t["amount"]) < 0
    ]
    return Summary(
        count=len(spending_transactions),
        total=sum(spending_transactions, Decimal("0"))
    )
```

**Checks:**

- Run `poetry run pytest test_main.py::TestGetSpendingSummary -v`
- All tests pass
