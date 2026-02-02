# Ticket 12: Add tests for print_report

**File:** `test_main.py`

Add tests for the `print_report` function (TDD red phase). This is the integration test.

**Actions:**

1. Import `print_report` from main
2. Create `TestPrintReport` class
3. Add test that captures stdout and verifies format matches README examples
4. Verify all four report sections are present

**Expected Output Format (from README):**

Note: README uses different formats for summaries vs categories:
- Income/Spending summaries: `{count} transactions, {amount}` (count first)
- Category breakdown: `{amount}, {count} transactions` (amount first!)

```
Income: 5 transactions, £5,023.95
Spending: 11 transactions, -£325.31
Shopping: -£136.30, 5 transactions - Bills and Utilities: -£69.86, 2 transactions - ...
WEB GENIUS: 3 transactions, £4,700.00
```

**Example:**

```python
from main import print_report


class TestPrintReport:
    def test_prints_all_sections(self, transactions: list[dict[str, str]], capsys) -> None:
        print_report(transactions)
        captured = capsys.readouterr()
        output = captured.out

        # Check income line (count first, then amount)
        assert "Income: 5 transactions, £5,023.95" in output

        # Check spending line (count first, then amount)
        assert "Spending: 11 transactions, -£325.31" in output

        # Check category breakdown (amount first, then count - per README example)
        assert "Shopping: -£136.30, 5 transactions" in output
        assert "Bills and Utilities: -£69.86, 2 transactions" in output

        # Check salary by payer
        assert "WEB GENIUS: 3 transactions, £4,700.00" in output

    def test_empty_transactions(self, capsys) -> None:
        print_report([])
        captured = capsys.readouterr()
        output = captured.out

        assert "Income: 0 transactions, £0.00" in output
        assert "Spending: 0 transactions, £0.00" in output
```

**Checks:**

- Tests exist and can be discovered by pytest
- Tests fail with ImportError or AssertionError (TDD red phase)
