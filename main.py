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
    if amount < 0:
        return f"-£{abs(amount):,.2f}"
    return f"£{amount:,.2f}"


def get_income_summary(transactions: list[dict[str, str]]) -> Summary:
    """Calculate total income (positive amounts) count and sum."""
    income_transactions = [
        Decimal(t["amount"])
        for t in transactions
        if Decimal(t["amount"]) > 0
    ]
    return Summary(
        count=len(income_transactions),
        total=sum(income_transactions, Decimal("0"))
    )


def get_spending_summary(transactions: list[dict[str, str]]) -> Summary:
    """Calculate total spending (negative amounts) count and sum."""
    spending_transactions = [
        Decimal(t["amount"])
        for t in transactions
        if Decimal(t["amount"]) < 0
    ]
    return Summary(
        count=len(spending_transactions),
        total=sum(spending_transactions, Decimal("0"))
    )


def get_spending_by_category(transactions: list[dict[str, str]]) -> list[CategorySummary]:
    """Break down spending by category."""
    categories: dict[str, list[Decimal]] = {}

    for t in transactions:
        amount = Decimal(t["amount"])
        if amount >= 0:
            continue

        category = t.get("category", "") or "Uncategorized"
        if category not in categories:
            categories[category] = []
        categories[category].append(amount)

    return [
        CategorySummary(
            category=cat,
            count=len(amounts),
            total=sum(amounts, Decimal("0"))
        )
        for cat, amounts in sorted(categories.items())
    ]


def get_salary_by_payer(transactions: list[dict[str, str]]) -> list[PayerSummary]:
    """Break down salary income by payer (from description field)."""
    payers: dict[str, list[Decimal]] = {}

    for t in transactions:
        if t.get("category", "") != "Salary":
            continue

        payer = t.get("description", "Unknown")
        amount = Decimal(t["amount"])

        if payer not in payers:
            payers[payer] = []
        payers[payer].append(amount)

    return [
        PayerSummary(
            payer=payer,
            count=len(amounts),
            total=sum(amounts, Decimal("0"))
        )
        for payer, amounts in sorted(payers.items())
    ]


def print_report(transactions: list[dict[str, str]]) -> None:
    """Print formatted transaction analysis report."""
    income = get_income_summary(transactions)
    print(f"Income: {income.count} transactions, {format_currency(income.total)}")

    spending = get_spending_summary(transactions)
    print(f"Spending: {spending.count} transactions, {format_currency(spending.total)}")

    categories = get_spending_by_category(transactions)
    if categories:
        category_parts = [
            f"{c.category}: {format_currency(c.total)}, {c.count} transactions"
            for c in categories
        ]
        print(" - ".join(category_parts))

    payers = get_salary_by_payer(transactions)
    for p in payers:
        print(f"{p.payer}: {p.count} transactions, {format_currency(p.total)}")
