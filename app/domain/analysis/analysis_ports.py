from abc import ABC, abstractmethod
from typing import List

from app.domain.analysis.analysis_models import AnalysisReport, Transaction


class AnalysisServicePort(ABC):

    @abstractmethod
    def analyze_transactions(self, transactions: List[Transaction]) -> AnalysisReport:
        raise NotImplementedError


class ReportRepositoryPort(ABC):

    @abstractmethod
    def save(self, report: AnalysisReport) -> None:
        raise NotImplementedError
