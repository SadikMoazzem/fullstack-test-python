# Transaction Analysis Research

## Problem Statement

Implement a bank transaction analysis system that processes CSV transaction data and produces aggregated summaries for income, spending, category breakdowns, and salary payer information. This is a TDD-focused task.

## Goals

- Calculate total income (count and sum of positive transactions)
- Calculate total spending (count and sum of negative transactions)
- Break down spending by category with counts and totals
- Break down salary income by payer (extracted from description)

## Non-Goals

- Persisting results to a database
- Building a UI or API
- Handling multiple currencies (all data is GBP)
- Real-time transaction processing

## Users/Consumers

- The `pytest` test runner consuming functions from `main.py`

---

## Requirements from User

The user specified the following requirements for this implementation:

### Currency Handling
Use `Decimal` for all currency calculations to avoid floating point precision errors:
```python
>>> 0.1 + 0.2
0.30000000000000004  # This is why we use Decimal
```

```python
from decimal import Decimal
amount = Decimal(row['amount'])  # Precise
```

### Type Safety
Full type hints on all functions for clarity and IDE support:
```python
from decimal import Decimal

def get_income_summary(transactions: list[dict[str, str]]) -> Summary:
    ...
```

### Dataclasses for Return Types
Use dataclasses instead of plain dicts:
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
```

### TDD Approach
Follow red→green→refactor cycle with tests written before implementation.

### Parametrized Tests
Use pytest parametrize for testing multiple cases:
```python
@pytest.mark.parametrize("amount,expected", [
    (Decimal("100.00"), "£100.00"),
    (Decimal("-50.50"), "-£50.50"),
    (Decimal("0"), "£0.00"),
    (Decimal("1234.56"), "£1,234.56"),
])
def test_format_currency(amount: Decimal, expected: str) -> None:
    assert format_currency(amount) == expected
```

### Empty Category Handling
Group transactions with empty category as "Uncategorized".

---

## Codebase Analysis

### Existing Patterns

The project provides a minimal scaffold:

| File | Purpose |
|------|---------|
| `main.py` | Contains stub function `normalise_transactions(transactions)` |
| `test_main.py` | Pytest setup with fixture loading CSV via `DictReader` |
| `transactions.csv` | 16 transactions (15 data rows) |

The test fixture already handles CSV parsing:
```python
@pytest.fixture
def transactions():
    with open("transactions.csv") as f:
        yield list(DictReader(f))
```

### Data Schema

**CSV Columns:**

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID string | Unique transaction ID |
| `created_at` | Timestamp | Creation time |
| `updated_at` | Timestamp | Last update time |
| `description` | String | Transaction description (payer for salary) |
| `amount` | Decimal string | Positive = income, Negative = spending |
| `currency_code` | String | Always "GBP" in dataset |
| `category` | String | May be empty |
| `date` | Timestamp | Transaction date |

### Data Analysis

**Transaction Counts:**
- Total: 16 transactions
- Income: 5 transactions, total £5,023.95
- Spending: 11 transactions, total -£325.31

**Categories Found:**
- Benefits: 1 transaction, £123.95
- Bills and Utilities: 2 transactions, -£69.86
- Food & Dining: 1 transaction, -£17.40
- Salary: 3 transactions, £4,700.00
- Shopping: 5 transactions, -£136.30
- Uncategorized: 4 transactions (mixed income/spending)

**Salary Payers:**
- WEB GENIUS: 3 transactions, £4,700.00

**Edge Cases:**
- 4 transactions have empty category field
- One uncategorized transaction is income (UBER: £200.00)
- Amount precision: 2 decimal places

---

## External Research

### Python CSV Best Practices

Source: [Python csv documentation](https://docs.python.org/3/library/csv.html)

- Use `newline=''` when opening CSV files for cross-platform compatibility
- `DictReader` returns all values as strings; explicit type conversion needed
- Iterator-based processing is memory-efficient

### TDD Patterns

Source: [Modern TDD in Python - TestDriven.io](https://testdriven.io/blog/modern-tdd/)

- Use GIVEN-WHEN-THEN structure for test clarity
- Test one behavior per test function
- Use `pytest.mark.parametrize` for multiple test cases

### UK Currency Formatting

Source: [AccountingWEB - UK formatting](https://www.accountingweb.co.uk/any-answers/psxxxx-or-psxxxx)

- Symbol left of amount, no space: `£1,234.56`
- Negative options: `-£325.31` (minus sign) or `(£325.31)` (parentheses)
- README example uses minus sign format: `-£1,500`

---

## Technical Analysis

### Approach Options

#### Option 1: Single Function with Multiple Returns

```python
def analyse_transactions(transactions):
    return {
        'income': {'count': 5, 'total': 5023.95},
        'spending': {'count': 11, 'total': -325.31},
        'spending_by_category': {...},
        'salary_by_payer': {...}
    }
```

**Pros:**
- Single entry point
- Easy to test as a whole

**Cons:**
- Large function, harder to unit test individual parts
- Violates Single Responsibility Principle

#### Option 2: Separate Functions per Requirement (Chosen)

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

def get_income_summary(transactions: list[dict[str, str]]) -> Summary
def get_spending_summary(transactions: list[dict[str, str]]) -> Summary
def get_spending_by_category(transactions: list[dict[str, str]]) -> list[CategorySummary]
def get_salary_by_payer(transactions: list[dict[str, str]]) -> list[PayerSummary]
def format_currency(amount: Decimal) -> str
def print_report(transactions: list[dict[str, str]]) -> None
```

**Pros:**
- Each function testable in isolation
- Follows TDD naturally (one test per function)
- Clear separation of concerns

**Cons:**
- More functions to maintain
- Repeated iteration over transactions (minor performance cost)

### Chosen Approach

**Option 2: Separate Functions** - This aligns better with TDD principles and makes testing straightforward. Performance is not a concern with 16 transactions.

### Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Function structure | Separate functions | Easier TDD, better testing |
| Numeric type | `Decimal` | Currency precision |
| Type hints | Full annotations | Modern Python; IDE support; self-documenting |
| Return types | Dataclasses | More Pythonic than dicts; type-safe |
| Uncategorized handling | "Uncategorized" string | Explicit handling of edge case |
| Payer extraction | Use full description | WEB GENIUS is the payer name |
| Negative format | `-£325.31` | Matches README example |
| Output | Both structured data + print | Separation of data and presentation |

---

## Implementation Considerations

### Dependencies

- Python 3.10+ (specified in pyproject.toml)
- pytest 9.0.2 (for testing)
- No external libraries for business logic (per requirements)

### Affected Areas

| File | Changes |
|------|---------|
| `main.py` | Implement all analysis functions |
| `test_main.py` | Add comprehensive tests for each function |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Currency precision | None | None | Using `Decimal` eliminates float errors |
| Empty category edge case | Low | Medium | Handle explicitly as "Uncategorized" |
| Test fixture coupling | Low | Low | Keep tests focused; use parameterized tests |

### Testing Strategy

**Unit Tests (Parametrized):**

| Function | Test Cases |
|----------|------------|
| `format_currency` | Positive, negative, zero, large numbers with commas |
| `get_income_summary` | Normal data, empty list, all spending (no income) |
| `get_spending_summary` | Normal data, empty list, all income (no spending) |
| `get_spending_by_category` | Multiple categories, uncategorized, single category |
| `get_salary_by_payer` | Multiple payers, single payer, no salary transactions |

**Edge Case Tests:**
- Empty transaction list
- Transaction with empty category → "Uncategorized"
- All transactions same category
- No salary transactions

**Integration Test:**
- Full report generation with actual CSV data
- Verify formatted output matches README examples

---

## Open Questions (Resolved)

- [x] How to handle empty category? → Group as "Uncategorized"
- [x] How to extract payer from salary? → Use description field
- [x] Output format? → Both structured data and print output

---

## Next Steps

1. Review and approve this research
2. Create detailed implementation plan
3. Implement using TDD approach (red-green-refactor)
