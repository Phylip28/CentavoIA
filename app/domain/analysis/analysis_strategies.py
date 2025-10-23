from abc import ABC, abstractmethod
from app.domain.analysis.analysis_models import Transaction, AnalysisReport
from typing import List, Dict

class AnalysisStrategy(ABC):
    
    @abstractmethod
    def analyze(self, transactions: List[Transaction], report: AnalysisReport) -> None:
        raise NotImplementedError()
    
class AntSpendingStrategy(AnalysisStrategy):

    def __init__(self, ant_threshold: float = 30.0):
        self._threshold = ant_threshold

    def analyze(self, transactions: List[Transaction], report: AnalysisReport) -> None:

        ant_spending_by_category: Dict[str, float] = {}
        total_ant_spending = 0.0

        for t in transactions:
            if t.amount <= self._threshold:
                ant_spending_by_category.setdefault(t.category, 0.0)
                ant_spending_by_category[t.category] += t.amount
                total_ant_spending += t.amount

        report.strategy_results["ant_spending"] = {
            "total_spent": total_ant_spending,
            "by_category": ant_spending_by_category
        }