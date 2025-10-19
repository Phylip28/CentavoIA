from .analysis_ports import AnalysisServicePort, ReportRepositoryPort
from typing import List
from .analysis_models import Transaction, AnalysisReport


class AnalyzeServiceImplementation(AnalysisServicePort):

    def __init__(self, repository: ReportRepositoryPort):
        self._repository = repository

    def analyze_transactions(self, transactions: List[Transaction]) -> AnalysisReport:

        total_spent = sum(t.monto for t in transactions)
        user_id = transactions[0].user_id if transactions else "Unknown"

        report = AnalysisReport(
            user_id=user_id,
            total_transaction=len(transactions),
            total_spent=total_spent,
        )

        self._repository.save(report)

        return report
