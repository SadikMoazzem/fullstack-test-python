# Ticket 2: Add tests for format_currency

**File:** `test_main.py`

Add parametrized tests for the `format_currency` function (TDD red phase).

**Actions:**

1. Remove the existing `normalise_transactions` import and test
2. Add import: `from decimal import Decimal`
3. Add import: `from main import format_currency`
4. Create `TestFormatCurrency` class with parametrized tests

**Example:**

```python
from csv import DictReader
from decimal import Decimal

import pytest

from main import format_currency


@pytest.fixture
def transactions():
    with open("transactions.csv") as f:
        yield list(DictReader(f))


class TestFormatCurrency:
    @pytest.mark.parametrize("amount,expected", [
        (Decimal("100.00"), "£100.00"),
        (Decimal("-50.50"), "-£50.50"),
        (Decimal("0"), "£0.00"),
        (Decimal("1234.56"), "£1,234.56"),
        (Decimal("-1234.56"), "-£1,234.56"),
        (Decimal("0.01"), "£0.01"),
    ])
    def test_formats_currency_correctly(self, amount: Decimal, expected: str) -> None:
        assert format_currency(amount) == expected
```

**Checks:**

- Tests exist and can be discovered by pytest
- Tests fail with ImportError or AssertionError (TDD red phase)
