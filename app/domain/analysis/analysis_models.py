from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict


class DomainError(Exception):
    """Base exception for domain errors."""
    pass


class EmptyTransactionListError(DomainError):
    """Attempted to analyze an empty list of transactions."""
    pass


@dataclass(frozen=True)
class Transaction:

    transaction_id: str
    amount: float
    date: date
    category: str
    user_id: str


@dataclass(frozen=True)
class AnalysisReport:

    user_id: str
    total_transaction: int
    total_spent: float
    strategy_results: Dict[str, Any] = field(default_factory=dict)
