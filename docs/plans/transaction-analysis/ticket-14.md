# Ticket 14: Run quality checks and final verification

**File:** `main.py` (verification only, no changes expected)

Run final quality checks to ensure the implementation is complete and correct.

**Actions:**

1. Run full test suite: `poetry run pytest -v`
2. Verify all tests pass
3. Check type hints are consistent (manual review)
4. Verify output matches README examples exactly
5. Review code for any cleanup opportunities

**Verification Commands:**

```bash
# Run all tests with verbose output
poetry run pytest -v

# Quick manual test
poetry run python -c "
from csv import DictReader
from main import print_report

with open('transactions.csv') as f:
    transactions = list(DictReader(f))
    print_report(transactions)
"
```

**Expected Output:**

```
Income: 5 transactions, £5,023.95
Spending: 11 transactions, -£325.31
Bills and Utilities: -£69.86, 2 transactions - Food & Dining: -£17.40, 1 transactions - Shopping: -£136.30, 5 transactions - Uncategorized: -£101.75, 3 transactions
WEB GENIUS: 3 transactions, £4,700.00
```

Note: Category format is `{amount}, {count} transactions` (amount first) per README example.

**Checks:**

- All tests pass (green)
- No type errors
- Output format matches README examples
- Code is clean and readable
