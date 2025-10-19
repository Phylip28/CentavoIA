from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Transaction:

    transaction_id: str
    amount: float
    date: date
    category: str
    user_id: str


@dataclass
class AnalysisReport:

    user_id: str
    total_transaction: int
    total_spent: float
