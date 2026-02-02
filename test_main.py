from csv import DictReader
from decimal import Decimal

import pytest

from main import (
    CategorySummary,
    format_currency,
    get_income_summary,
    get_salary_by_payer,
    get_spending_by_category,
    get_spending_summary,
    PayerSummary,
    print_report,
    Summary,
)


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


class TestGetIncomeSummary:
    def test_returns_correct_count_and_total(self, transactions: list[dict[str, str]]) -> None:
        result = get_income_summary(transactions)
        assert isinstance(result, Summary)
        assert result.count == 5
        assert result.total == Decimal("5023.95")

    def test_empty_list_returns_zero(self) -> None:
        result = get_income_summary([])
        assert result.count == 0
        assert result.total == Decimal("0")

    def test_all_spending_returns_zero(self) -> None:
        spending_only = [{"amount": "-100.00"}, {"amount": "-50.00"}]
        result = get_income_summary(spending_only)
        assert result.count == 0
        assert result.total == Decimal("0")


class TestGetSpendingSummary:
    def test_returns_correct_count_and_total(self, transactions: list[dict[str, str]]) -> None:
        result = get_spending_summary(transactions)
        assert isinstance(result, Summary)
        assert result.count == 11
        assert result.total == Decimal("-325.31")

    def test_empty_list_returns_zero(self) -> None:
        result = get_spending_summary([])
        assert result.count == 0
        assert result.total == Decimal("0")

    def test_all_income_returns_zero(self) -> None:
        income_only = [{"amount": "100.00"}, {"amount": "50.00"}]
        result = get_spending_summary(income_only)
        assert result.count == 0
        assert result.total == Decimal("0")


class TestGetSpendingByCategory:
    def test_returns_correct_breakdown(self, transactions: list[dict[str, str]]) -> None:
        result = get_spending_by_category(transactions)
        assert all(isinstance(r, CategorySummary) for r in result)

        by_category = {r.category: r for r in result}

        assert by_category["Shopping"].count == 5
        assert by_category["Shopping"].total == Decimal("-136.30")

        assert by_category["Bills and Utilities"].count == 2
        assert by_category["Bills and Utilities"].total == Decimal("-69.86")

        assert by_category["Food & Dining"].count == 1
        assert by_category["Food & Dining"].total == Decimal("-17.40")

    def test_empty_category_becomes_uncategorized(self, transactions: list[dict[str, str]]) -> None:
        result = get_spending_by_category(transactions)
        by_category = {r.category: r for r in result}

        assert "Uncategorized" in by_category
        assert by_category["Uncategorized"].count == 3
        assert by_category["Uncategorized"].total == Decimal("-101.75")

    def test_empty_list_returns_empty(self) -> None:
        result = get_spending_by_category([])
        assert result == []


class TestGetSalaryByPayer:
    def test_returns_correct_breakdown(self, transactions: list[dict[str, str]]) -> None:
        result = get_salary_by_payer(transactions)
        assert all(isinstance(r, PayerSummary) for r in result)

        assert len(result) == 1
        assert result[0].payer == "WEB GENIUS"
        assert result[0].count == 3
        assert result[0].total == Decimal("4700.00")

    def test_empty_list_returns_empty(self) -> None:
        result = get_salary_by_payer([])
        assert result == []

    def test_no_salary_transactions_returns_empty(self) -> None:
        non_salary = [
            {"amount": "100.00", "category": "Benefits", "description": "REBATE"},
            {"amount": "-50.00", "category": "Shopping", "description": "STORE"},
        ]
        result = get_salary_by_payer(non_salary)
        assert result == []

    def test_multiple_payers(self) -> None:
        multi_payer = [
            {"amount": "1000.00", "category": "Salary", "description": "COMPANY A"},
            {"amount": "500.00", "category": "Salary", "description": "COMPANY B"},
            {"amount": "1000.00", "category": "Salary", "description": "COMPANY A"},
        ]
        result = get_salary_by_payer(multi_payer)
        by_payer = {r.payer: r for r in result}

        assert by_payer["COMPANY A"].count == 2
        assert by_payer["COMPANY A"].total == Decimal("2000.00")
        assert by_payer["COMPANY B"].count == 1
        assert by_payer["COMPANY B"].total == Decimal("500.00")


class TestPrintReport:
    def test_prints_all_sections(self, transactions: list[dict[str, str]], capsys) -> None:
        print_report(transactions)
        captured = capsys.readouterr()
        output = captured.out

        assert "Income: 5 transactions, £5,023.95" in output
        assert "Spending: 11 transactions, -£325.31" in output
        assert "Shopping: -£136.30, 5 transactions" in output
        assert "Bills and Utilities: -£69.86, 2 transactions" in output
        assert "WEB GENIUS: 3 transactions, £4,700.00" in output

    def test_empty_transactions(self, capsys) -> None:
        print_report([])
        captured = capsys.readouterr()
        output = captured.out

        assert "Income: 0 transactions, £0.00" in output
        assert "Spending: 0 transactions, £0.00" in output
