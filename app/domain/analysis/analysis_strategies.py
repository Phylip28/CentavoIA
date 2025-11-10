import math
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date, timedelta
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
            "total_spent": round(total_ant_spending, 2),
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


class RecurrenceStrategy(AnalysisStrategy):
    def __init__(self, day_tolerance: int = 3, amount_tolerance_percent: float = 0.10):
        self.strategy_name = "recurrence_analysis"
        self.intervals = {
            "monthly": (timedelta(days=30), timedelta(days=day_tolerance)),
            "weekly": (timedelta(days=7), timedelta(days=day_tolerance // 2 or 1)),
        }
        self.amount_tolerance = amount_tolerance_percent

    def analyze(self, transactions: List[Transaction]) -> Tuple[str, Any]:
        categorized_transactions: Dict[str, List[Transaction]] = defaultdict(list)
        for t in transactions:
            categorized_transactions[t.category].append(t)

        found_recurrences = []

        for category, trans in categorized_transactions.items():
            if len(trans) < 2:
                continue

            sorted_trans = sorted(trans, key=lambda t: t.date)

            for i in range(len(sorted_trans)):
                for j in range(i + 1, len(sorted_trans)):
                    t1 = sorted_trans[i]
                    t2 = sorted_trans[j]

                    if not math.isclose(
                        t1.amount, t2.amount, rel_tol=self.amount_tolerance
                    ):
                        continue

                    time_delta = abs(t2.date - t1.date)

                    for interval_name, (
                        base_delta,
                        tolerance_delta,
                    ) in self.intervals.items():
                        if (
                            (base_delta - tolerance_delta)
                            <= time_delta
                            <= (base_delta + tolerance_delta)
                        ):
                            found_recurrences.append(
                                {
                                    "type": interval_name,
                                    "category": category,
                                    "amount": t1.amount,
                                    "date1": t1.date.isoformat(),
                                    "date2": t2.date.isoformat(),
                                }
                            )

        results = {
            "potential_recurrences_found": len(found_recurrences),
            "details": found_recurrences,
        }

        return (self.strategy_name, results)
