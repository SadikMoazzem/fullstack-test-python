# Ticket 3: Implement format_currency

**File:** `main.py`

Implement the `format_currency` function to make the tests from ticket 2 pass.

**Actions:**

1. Add `format_currency(amount: Decimal) -> str` function
2. Handle positive amounts: `£1,234.56`
3. Handle negative amounts: `-£1,234.56`
4. Handle zero: `£0.00`
5. Always show 2 decimal places
6. Use comma as thousands separator

**Example:**

```python
def format_currency(amount: Decimal) -> str:
    """Format a Decimal amount as GBP currency string."""
    if amount < 0:
        return f"-£{abs(amount):,.2f}"
    return f"£{amount:,.2f}"
```

**Checks:**

- Run `poetry run pytest test_main.py::TestFormatCurrency -v`
- All parametrized tests pass
