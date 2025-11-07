import json
import logging
from dataclasses import asdict
from app.domain.analysis.analysis_ports import ReportRepositoryPort
from app.domain.analysis.analysis_models import AnalysisReport

log = logging.getLogger(__name__)


class LogginReportRepository(ReportRepositoryPort):

    def save(self, report: AnalysisReport) -> None:

        report_dict = asdict(report)

        log.info(
            "--- SAVING ANALYSIS REPORT ---\n%s",
            json.dumps(report_dict, indent=2, default=str)
        )
