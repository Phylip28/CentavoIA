from typing import List

from app.adapters.persistence.analysis.sql_report_repository import (
    SQLAlchemyReportRepository,
)
from app.adapters.persistence.database import SessionLocal
from app.core.config import settings
from app.domain.analysis.analysis_ports import AnalysisServicePort
from app.domain.analysis.analysis_service import AnalyzeServiceImplementation
from app.domain.analysis.analysis_strategies import (
    AnalysisStrategy,
    AntSpendingStrategy,
    PeakSpendingStrategy,
    RecurrenceStrategy,
)


def create_analysis_service() -> AnalysisServicePort:
    """
    Fábrica (Factory) para el Servicio de Análisis.

    Construye el servicio con todas sus dependencias concretas.
    Esta lógica se extrae de main.py para que pueda ser
    reutilizada por los workers de Celery.
    """

    repository = SQLAlchemyReportRepository(session_factory=SessionLocal)

    active_strategies: List[AnalysisStrategy] = [
        AntSpendingStrategy(ant_threshold=settings.ANT_SPENDING_THRESHOLD),
        PeakSpendingStrategy(peak_threshold=settings.PEAK_SPENDING_THRESHOLD),
        RecurrenceStrategy(
            day_tolerance=settings.RECURRENCE_DAY_TOLERANCE,
            amount_tolerance_percent=settings.RECURRENCE_AMOUNT_TOLERANCE,
        ),
    ]

    service = AnalyzeServiceImplementation(
        repository=repository, strategies=active_strategies
    )

    return service
