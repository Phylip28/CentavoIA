from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date
from typing import Any, Dict, List, Tuple

from app.domain.analysis.analysis_models import Transaction


class AnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, transactions: List[Transaction]) -> Tuple[str, Any]:
        raise NotImplementedError()


class AntSpendingStrategy(AnalysisStrategy):
    def __init__(self, ant_threshold: float = 30.0):
        self._threshold = ant_threshold
        self.strategy_name = "ant_spending"

    def analyze(self, transactions: List[Transaction]) -> Tuple[str, Any]:
        ant_spending_by_category: Dict[str, float] = {}
        total_ant_spending = 0.0

        for t in transactions:
            if t.amount <= self._threshold:
                ant_spending_by_category.setdefault(t.category, 0.0)
                ant_spending_by_category[t.category] += t.amount
                total_ant_spending += t.amount

        results = {
            "total_spent": total_ant_spending,
            "by_category": ant_spending_by_category,
        }

        return (self.strategy_name, results)


class PeakSpendingStrategy(AnalysisStrategy):
    def __init__(self, peak_threshold: float = 150.0):
        self._threshold = peak_threshold
        self.strategy_name = "peak_spending"

    def analyze(self, transactions: List[Transaction]) -> Tuple[str, Any]:
        # Usamos defaultdict para facilitar la suma
        daily_totals: Dict[date, float] = defaultdict(float)

        # 1. Agrupar gastos por día
        for t in transactions:
            daily_totals[t.date] += t.amount

        peak_days = []
        for day, total in daily_totals.items():
            if total > self._threshold:
                peak_days.append(
                    {
                        "date": day.isoformat(),
                        "total_spent": total,
                        "threshold": self._threshold,
                    }
                )

        results = {"peak_days_found": len(peak_days), "peaks": peak_days}

        return (self.strategy_name, results)
