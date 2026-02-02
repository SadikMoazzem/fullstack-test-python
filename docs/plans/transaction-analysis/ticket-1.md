# Ticket 1: Add dataclasses and type definitions

**File:** `main.py`

Create the dataclass definitions and type aliases that will be used throughout the implementation.

**Actions:**

1. **REMOVE** the existing `normalise_transactions` stub function (it's unused and will cause import errors)
2. Add imports: `from dataclasses import dataclass` and `from decimal import Decimal`
3. Create `Summary` dataclass with fields: `count: int`, `total: Decimal`
4. Create `CategorySummary` dataclass with fields: `category: str`, `count: int`, `total: Decimal`
5. Create `PayerSummary` dataclass with fields: `payer: str`, `count: int`, `total: Decimal`

**Example:**

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Summary:
    count: int
    total: Decimal


@dataclass
class CategorySummary:
    category: str
    count: int
    total: Decimal


@dataclass
class PayerSummary:
    payer: str
    count: int
    total: Decimal
```

**Checks:**

- File imports successfully: `from main import Summary, CategorySummary, PayerSummary`
- Dataclasses can be instantiated: `Summary(count=1, total=Decimal("100.00"))`
