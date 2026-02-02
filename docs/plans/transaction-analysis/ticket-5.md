# Ticket 5: Implement get_income_summary

**File:** `main.py`

Implement the `get_income_summary` function to make tests pass.

**Actions:**

1. Add `get_income_summary(transactions: list[dict[str, str]]) -> Summary` function
2. Filter transactions where amount > 0
3. Count and sum the filtered transactions
4. Return a Summary dataclass instance

**Example:**

```python
def get_income_summary(transactions: list[dict[str, str]]) -> Summary:
    """Calculate total income (positive amounts) count and sum."""
    income_transactions = [
        Decimal(t["amount"])
        for t in transactions
        if Decimal(t["amount"]) > 0
    ]
    return Summary(
        count=len(income_transactions),
        total=sum(income_transactions, Decimal("0"))
    )
```

**Checks:**

- Run `poetry run pytest test_main.py::TestGetIncomeSummary -v`
- All tests pass
