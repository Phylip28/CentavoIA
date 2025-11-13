import logging
from typing import Any, Dict, List

from app.domain.analysis.analysis_models import (
    AnalysisReport,
    EmptyTransactionListError,
    Transaction,
)
from app.domain.analysis.analysis_ports import AnalysisServicePort, ReportRepositoryPort
from app.domain.analysis.analysis_strategies import AnalysisStrategy

log = logging.getLogger(__name__)


class AnalyzeServiceImplementation(AnalysisServicePort):
    def __init__(
        self, repository: ReportRepositoryPort, strategies: List[AnalysisStrategy]
    ):
        self._repository = repository
        self._strategies = strategies

    def analyze_transactions(
        self, transactions: List[Transaction], job_id: str
    ) -> AnalysisReport:
        if not transactions:
            log.warning("Tried to analyze an empty list of transactions.")
            raise EmptyTransactionListError()

        log.info(f"Start analysis of {len(self._strategies)} strategies")

        total_spent = sum(t.amount for t in transactions)
        user_id = transactions[0].user_id

        strategy_results: Dict[str, Any] = {}
        for strategy in self._strategies:
            strategy_name, result = strategy.analyze(transactions)
            strategy_results[strategy_name] = result

        report = AnalysisReport(
            job_id=job_id,
            user_id=user_id,
            total_transactions=len(transactions),
            total_spent=total_spent,
            strategy_results=strategy_results,
        )

        self._repository.save(report)
        log.info("Analysis complete and save.")

        return report
