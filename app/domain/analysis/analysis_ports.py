from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.analysis.analysis_models import AnalysisReport, Transaction


class AnalysisServicePort(ABC):
    @abstractmethod
    def analyze_transactions(
        self, transactions: List[Transaction], job_id: str
    ) -> AnalysisReport:
        raise NotImplementedError


class ReportRepositoryPort(ABC):
    @abstractmethod
    def save(self, report: AnalysisReport) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_job_id(self, job_id: str) -> Optional[AnalysisReport]:
        raise NotImplementedError
