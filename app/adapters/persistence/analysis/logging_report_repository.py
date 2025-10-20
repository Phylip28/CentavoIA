import json
from dataclasses import asdict
from app.domain.analysis.analysis_ports import ReportRepositoryPort
from app.domain.analysis.analysis_models import AnalysisReport

class LogginReportRepository(ReportRepositoryPort):

    def save(self, report: AnalysisReport) -> None:
        
        report_dict = asdict(report)

        print(json.dumps(report_dict, indent=2, default=str))