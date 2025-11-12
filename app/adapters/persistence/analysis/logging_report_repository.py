import json
import logging
from dataclasses import asdict
from typing import Optional

from app.domain.analysis.analysis_models import AnalysisReport
from app.domain.analysis.analysis_ports import ReportRepositoryPort

log = logging.getLogger(__name__)


class LogginReportRepository(ReportRepositoryPort):
    def save(self, report: AnalysisReport) -> None:
        report_dict = asdict(report)

        log.info(
            "--- SAVING ANALYSIS REPORT ---\n%s",
            json.dumps(report_dict, indent=2, default=str),
        )

    def get_by_job_id(self, job_id: str) -> Optional[AnalysisReport]:
        """
        The logging repository does not store data, so it cannot 'retrieve'.
        """
        log.warning(
            f"Attempt to retrieve job_id '{job_id}' from LoggingReportRepository. "
            "This adapter does not support reads."
        )
        return None
