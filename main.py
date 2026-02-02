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


def format_currency(amount: Decimal) -> str:
    """Format a Decimal amount as GBP currency string."""
    pass


def get_income_summary(transactions: list[dict[str, str]]) -> Summary:
    """Calculate total income (positive amounts) count and sum."""
    pass


def get_spending_summary(transactions: list[dict[str, str]]) -> Summary:
    """Calculate total spending (negative amounts) count and sum."""
    pass


def get_spending_by_category(transactions: list[dict[str, str]]) -> list[CategorySummary]:
    """Break down spending by category."""
    pass


def get_salary_by_payer(transactions: list[dict[str, str]]) -> list[PayerSummary]:
    """Break down salary income by payer (from description field)."""
    pass


def print_report(transactions: list[dict[str, str]]) -> None:
    """Print formatted transaction analysis report."""
    pass
