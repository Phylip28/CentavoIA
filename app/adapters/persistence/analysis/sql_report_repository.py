from typing import Callable

from sqlalchemy.orm import Session

from app.domain.analysis.analysis_models import AnalysisReport
from app.domain.analysis.analysis_ports import ReportRepositoryPort

from .report_model import ReportModel


class SQLAlchemyReportRepository(ReportRepositoryPort):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def save(self, report: AnalysisReport) -> None:
        with self.session_factory() as session:
            db_report = ReportModel(
                user_id=report.user_id,
                total_transactions=report.total_transactions,
                total_spent=report.total_spent,
                strategy_results=report.strategy_results,
            )

            session.add(db_report)
            session.commit()
