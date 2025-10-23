from dataclasses import dataclass, field
from datetime import date
from typing import Dict, Any


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
    strategy_results: Dict[str, Any] = field(default_factory=dict)
