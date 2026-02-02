# Transaction Analysis Implementation Plan

## Overview

Implement a bank transaction analysis system using TDD that processes CSV transaction data and produces aggregated summaries for income, spending, category breakdowns, and salary payer information. Uses Decimal for currency precision, type hints, dataclasses, and parametrized tests.

## Assumptions

- All amounts are in GBP (no multi-currency support needed)
- Empty category fields should be grouped as "Uncategorized"
- Salary payer is extracted from the `description` field
- Output format: both structured data (dataclasses) and formatted print output

## Dependencies

- Python 3.10+ (for modern type hint syntax)
- pytest 9.0.2 (already installed via Poetry)
- Standard library only: `decimal`, `dataclasses`, `csv`

## Reference

- Research document: [transaction-analysis_research.md](transaction-analysis_research.md)

---

## Tickets

| Status | ID | Phase | Agent | Deps | Description |
|--------|----|-------|-------|------|-------------|
| [x] | 1 | 1 | execute-ticket-low | - | Add dataclasses and type definitions |
| [x] | 2 | 2 | execute-ticket-low | 1 | Add tests for format_currency |
| [x] | 3 | 2 | execute-ticket-low | 1,2 | Implement format_currency |
| [x] | 4 | 3 | execute-ticket-low | 2 | Add tests for get_income_summary |
| [x] | 5 | 3 | execute-ticket-low | 1,4 | Implement get_income_summary |
| [x] | 6 | 4 | execute-ticket-low | 4 | Add tests for get_spending_summary |
| [x] | 7 | 4 | execute-ticket-low | 5,6 | Implement get_spending_summary |
| [x] | 8 | 5 | execute-ticket-medium | 6 | Add tests for get_spending_by_category |
| [x] | 9 | 5 | execute-ticket-medium | 7,8 | Implement get_spending_by_category |
| [x] | 10 | 6 | execute-ticket-medium | 8 | Add tests for get_salary_by_payer |
| [x] | 11 | 6 | execute-ticket-medium | 9,10 | Implement get_salary_by_payer |
| [x] | 12 | 7 | execute-ticket-low | 10 | Add tests for print_report |
| [x] | 13 | 7 | execute-ticket-medium | 11,12 | Implement print_report |
| [x] | 14 | 8 | execute-ticket-low | 13 | Run quality checks and final verification |

---

## Execution Notes

### TDD Flow

This plan follows strict TDD discipline:
- **Test tickets** (even IDs 2,4,6,8,10,12) write failing tests first
- **Implementation tickets** (odd IDs 3,5,7,9,11,13) make tests pass
- Each phase completes a red→green cycle for one function

### Commit Strategy

After each ticket completes, commit with appropriate message:
- Test tickets: `feat(test): add failing test for [function]`
- Implementation tickets: `feat: implement [function]`
- Quality ticket: `chore: run quality checks`

### Expected Final Structure

```
main.py
├── Dataclasses: Summary, CategorySummary, PayerSummary
├── format_currency(amount: Decimal) -> str
├── get_income_summary(transactions) -> Summary
├── get_spending_summary(transactions) -> Summary
├── get_spending_by_category(transactions) -> list[CategorySummary]
├── get_salary_by_payer(transactions) -> list[PayerSummary]
└── print_report(transactions) -> None

test_main.py
├── Fixtures: transactions, empty_transactions, etc.
├── TestFormatCurrency (parametrized)
├── TestGetIncomeSummary
├── TestGetSpendingSummary
├── TestGetSpendingByCategory
├── TestGetSalaryByPayer
└── TestPrintReport (integration)
```
