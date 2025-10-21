from fastapi import FastAPI
from app.domain.analysis.analysis_ports import AnalysisServicePort
from app.adapters.persistence.analysis.logging_report_repository import LogginReportRepository
from app.domain.analysis.analysis_service import AnalyzeServiceImplementation
from app.adapters.api.analysis import analysis_controller

app = FastAPI(
    title="Centavo IA Analysis Module",
    description="Analysis Service for Expense Patterns",
    version="0.1.0"
)

def createAnalysisService() -> AnalysisServicePort:
    
    repository = LogginReportRepository()
    service = AnalyzeServiceImplementation(repository=repository)

    return service

app.dependency_overrides[analysis_controller.get_analysis_service] = createAnalysisService

app.include_router(analysis_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Centavo IA Analyssis Service"}