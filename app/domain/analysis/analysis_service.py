from app.domain.analysis.analysis_ports import AnalysisServicePort, ReportRepositoryPort
from typing import List
from app.domain.analysis.analysis_models import Transaction, AnalysisReport
from app.domain.analysis.analysis_strategies import AnalysisStrategy


class AnalyzeServiceImplementation(AnalysisServicePort):

    def __init__(self, repository: ReportRepositoryPort, strategies: List[AnalysisStrategy]):
        self._repository = repository
        self._strategies = strategies

    def analyze_transactions(self, transactions: List[Transaction]) -> AnalysisReport:

        print(f"Start analysis of {len(self._strategies)} strategies")

        total_spent = sum(t.amount for t in transactions)
        user_id = transactions[0].user_id if transactions else "Unknown"

        report = AnalysisReport(
            user_id=user_id,
            total_transaction=len(transactions),
            total_spent=total_spent,
        )

        for strategy in self._strategies:
            strategy.analyze(transactions=transactions, report=report)

        self._repository.save(report)

        return report
