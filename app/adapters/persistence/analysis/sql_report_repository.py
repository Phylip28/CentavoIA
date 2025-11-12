from typing import Callable, Optional

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
                job_id=report.job_id,
                user_id=report.user_id,
                total_transactions=report.total_transactions,
                total_spent=report.total_spent,
                strategy_results=report.strategy_results,
            )

            session.add(db_report)
            session.commit()

    def get_by_job_id(self, job_id: str) -> Optional[AnalysisReport]:
        with self.session_factory() as session:
            db_report: Optional[ReportModel] = session.get(ReportModel, job_id)

            if not db_report:
                return None

            return AnalysisReport(
                job_id=db_report.job_id,
                user_id=db_report.user_id,
                total_transactions=db_report.total_transactions,
                total_spent=db_report.total_spent,
                strategy_results=db_report.strategy_results,
            )
