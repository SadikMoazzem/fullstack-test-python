# Approach

This document explains my approach to completing the transaction analysis task.

## Process Overview

```
Research → Plan → Review → Execute → Verify
```

### 1. Research Phase

Before writing any code, I used a custom Claude skill (`/research-plan`) to conduct thorough research. The skill uses the Socratic method - it asks clarifying questions and proposes research actions for my approval before executing.

Through this guided process, we:

- **Analysed the CSV data** to understand the actual transaction structure
- **Identified edge cases** (empty categories, negative amounts, multiple payers)
- **Made technical decisions** upfront based on my requirements
- **Documented findings** in `docs/plans/transaction-analysis/transaction-analysis_research.md`

Key questions answered during the research dialogue:
- What data types are we dealing with? (strings from CSV)
- What precision is needed for currency? (Decimal, not float)
- How should empty categories be handled? (as "Uncategorized")
- What format does the README expect? (UK currency with £ symbol)

### 2. Planning Phase

I used a custom Claude skill (`/create-plan`) to generate a detailed implementation plan. The skill:

- **Breaks down work** into small, testable units automatically
- **Orders tickets** to follow TDD (tests before implementation)
- **Generates exact actions** for each ticket with verification commands
- **Includes code examples** to ensure consistency

My role was to **guide the skill** with my requirements (Decimal, TDD, etc.) and **review the output** before approving. The skill produced 14 tickets across 8 phases.

The plan is in `docs/plans/transaction-analysis/transaction-analysis_plan.md` with individual tickets in `ticket-1.md` through `ticket-14.md`.

### 3. Review Phase

Before execution, I had the plan reviewed using a code review agent:

- **Checked against requirements** - Does it cover all README examples?
- **Verified TDD structure** - Are tests written before implementations?
- **Validated technical decisions** - Is Decimal used consistently?
- **Made adjustments** based on review findings

I manually reviewed the agent's feedback and made changes to the plan before approving execution. The review checklist is in `docs/plans/transaction-analysis/transaction-analysis_plan_review.md`.

### 4. Execution Phase

I used a custom execution skill (`/execute-plan`) that orchestrates AI agents to work through tickets:

- **Parallel execution** - Independent tickets run simultaneously via sub-agents
- **Model selection** - Simpler tickets use faster/cheaper models (Haiku), complex ones use more capable models (Sonnet/Opus)
- **Built-in verification** - Every ticket has check commands that agents must run
- **Automatic validation** - Agents verify their work passes before marking complete
- **Human oversight** - I monitored progress and reviewed outputs

Each agent executes its ticket, runs the verification commands, and only reports success if all checks pass. This ensures quality while maximising efficiency through parallelisation.

### 5. Verification Phase

Final checks ensured everything works correctly:

```bash
poetry run pytest -v  # All 21 tests pass
```

---

## TDD Approach

I followed strict Test-Driven Development:

### Red Phase (Commit 1)
Write failing tests first:
```bash
git log --oneline
# 330fdf8 feat(test): add failing tests for transaction analysis (TDD red phase)
```

Tests define the expected behaviour before any implementation exists.

### Green Phase (Commit 2)
Write minimal code to make tests pass:
```bash
# f402c12 feat: implement transaction analysis functions (TDD green phase)
```

Focus on correctness, not perfection.

### Refactor Phase (Commit 3)
Clean up while keeping tests green:
```bash
# 6d8d336 chore: add documentation and section comments
```

Improve code quality without changing behaviour.

---

## Testing Strategy

### Test Structure

```
21 tests across 6 test classes:
├── TestFormatCurrency (6 parametrized tests)
├── TestGetIncomeSummary (3 tests)
├── TestGetSpendingSummary (3 tests)
├── TestGetSpendingByCategory (3 tests)
├── TestGetSalaryByPayer (4 tests)
└── TestPrintReport (2 integration tests)
```

### Test Types

1. **Unit tests** - Test individual functions in isolation
2. **Parametrized tests** - Cover multiple cases efficiently
3. **Edge case tests** - Empty lists, no matching transactions
4. **Integration tests** - `print_report` tests the full flow

### Fixtures

Used pytest fixtures for shared test data:
```python
@pytest.fixture
def transactions() -> list[dict[str, str]]:
    """Load real transaction data for tests."""
    with open("transactions.csv") as f:
        return list(DictReader(f))
```

---

## How to Run

```bash
# Install dependencies
poetry install

# Run all tests
poetry run pytest -v

# Run specific test class
poetry run pytest test_main.py::TestFormatCurrency -v

# Run the report
poetry run python -c "
from csv import DictReader
from main import print_report

with open('transactions.csv') as f:
    transactions = list(DictReader(f))
    print_report(transactions)
"
```

Expected output:
```
Income: 5 transactions, £5,023.95
Spending: 11 transactions, -£325.31
Bills and Utilities: -£69.86, 2 transactions - Food & Dining: -£17.40, 1 transactions - Shopping: -£136.30, 5 transactions - Uncategorized: -£101.75, 3 transactions
WEB GENIUS: 3 transactions, £4,700.00
```