# Ticket 13: Implement print_report

**File:** `main.py`

Implement the `print_report` function to make tests pass. This brings together all other functions.

**Actions:**

1. Add `print_report(transactions: list[dict[str, str]]) -> None` function
2. Call `get_income_summary` and format output
3. Call `get_spending_summary` and format output
4. Call `get_spending_by_category` and format output (dash-separated)
5. Call `get_salary_by_payer` and format output
6. Print all formatted lines

**Output Format (matching README examples):**

Note: README uses different formats:
- Income/Spending summaries: `{count} transactions, {amount}` (count first)
- Category breakdown: `{amount}, {count} transactions` (amount first!)

```
Income: {count} transactions, {formatted_total}
Spending: {count} transactions, {formatted_total}
{category}: {formatted_total}, {count} transactions - {category2}: ...
{payer}: {count} transactions, {formatted_total}
```

**Example:**

```python
def print_report(transactions: list[dict[str, str]]) -> None:
    """Print formatted transaction analysis report."""
    # Income summary (count first, then amount)
    income = get_income_summary(transactions)
    print(f"Income: {income.count} transactions, {format_currency(income.total)}")

    # Spending summary (count first, then amount)
    spending = get_spending_summary(transactions)
    print(f"Spending: {spending.count} transactions, {format_currency(spending.total)}")

    # Spending by category (AMOUNT FIRST, then count - per README example)
    categories = get_spending_by_category(transactions)
    if categories:
        category_parts = [
            f"{c.category}: {format_currency(c.total)}, {c.count} transactions"
            for c in categories
        ]
        print(" - ".join(category_parts))

    # Salary by payer
    payers = get_salary_by_payer(transactions)
    for p in payers:
        print(f"{p.payer}: {p.count} transactions, {format_currency(p.total)}")
```

**Checks:**

- Run `poetry run pytest test_main.py::TestPrintReport -v`
- All tests pass
- Run `poetry run pytest` to verify all tests pass
