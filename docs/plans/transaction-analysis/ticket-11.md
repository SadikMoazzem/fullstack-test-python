# Ticket 11: Implement get_salary_by_payer

**File:** `main.py`

Implement the `get_salary_by_payer` function to make tests pass.

**Actions:**

1. Add `get_salary_by_payer(transactions: list[dict[str, str]]) -> list[PayerSummary]` function
2. Filter to only transactions where category == "Salary"
3. Group by description (payer name)
4. For each payer, calculate count and total
5. Return list of PayerSummary instances

**Example:**

```python
def get_salary_by_payer(transactions: list[dict[str, str]]) -> list[PayerSummary]:
    """Break down salary income by payer (from description field)."""
    payers: dict[str, list[Decimal]] = {}

    for t in transactions:
        if t.get("category", "") != "Salary":
            continue

        payer = t.get("description", "Unknown")
        amount = Decimal(t["amount"])

        if payer not in payers:
            payers[payer] = []
        payers[payer].append(amount)

    return [
        PayerSummary(
            payer=payer,
            count=len(amounts),
            total=sum(amounts, Decimal("0"))
        )
        for payer, amounts in sorted(payers.items())
    ]
```

**Checks:**

- Run `poetry run pytest test_main.py::TestGetSalaryByPayer -v`
- All tests pass
