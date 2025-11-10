import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI

from app.adapters.api.analysis import analysis_controller
from app.adapters.persistence.analysis.sql_report_repository import (
    SQLAlchemyReportRepository,
)
from app.adapters.persistence.database import Base, SessionLocal, engine
from app.core.config import settings
from app.domain.analysis.analysis_ports import AnalysisServicePort
from app.domain.analysis.analysis_service import AnalyzeServiceImplementation
from app.domain.analysis.analysis_strategies import (
    AnalysisStrategy,
    AntSpendingStrategy,
    PeakSpendingStrategy,
    RecurrenceStrategy,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Centavo IA Analysis Module",
    description="Analysis Service for Expense Patterns",
    version="0.1.0",
    lifespan=lifespan,
)


def createAnalysisService() -> AnalysisServicePort:
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


app.dependency_overrides[analysis_controller.get_analysis_service] = (
    createAnalysisService
)

app.include_router(analysis_controller.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Centavo IA Analyssis Service"}
