import logging
from typing import List

from fastapi import FastAPI

from app.adapters.api.analysis import analysis_controller
from app.adapters.persistence.analysis.logging_report_repository import (
    LogginReportRepository,
)
from app.core.config import settings
from app.domain.analysis.analysis_ports import AnalysisServicePort
from app.domain.analysis.analysis_service import AnalyzeServiceImplementation
from app.domain.analysis.analysis_strategies import (
    AnalysisStrategy,
    AntSpendingStrategy,
)

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Centavo IA Analysis Module",
    description="Analysis Service for Expense Patterns",
    version="0.1.0"
)


def createAnalysisService() -> AnalysisServicePort:

    repository = LogginReportRepository()

    active_strategies: List[AnalysisStrategy] = [
        AntSpendingStrategy(ant_threshold=settings.ANT_SPENDING_THRESHOLD)
    ]
    service = AnalyzeServiceImplementation(
        repository=repository, strategies=active_strategies
    )

    return service


app.dependency_overrides[
    analysis_controller.get_analysis_service
] = createAnalysisService

app.include_router(analysis_controller.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Centavo IA Analyssis Service"}
