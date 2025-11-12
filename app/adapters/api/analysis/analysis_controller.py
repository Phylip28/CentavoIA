from typing import List

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, status

from app.adapters.api.analysis.analysis_schema import (
    AnalysisJobSchema,
    AnalysisReportSchema,
    JobStatusSchema,
    TransactionSchema,
)
from app.core.celery_app import celery_app
from app.core.dependencies import get_report_repository
from app.domain.analysis.analysis_ports import ReportRepositoryPort
from app.domain.analysis.tasks import run_analysis_task

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post(
    "/", response_model=AnalysisJobSchema, status_code=status.HTTP_202_ACCEPTED
)
async def start_analysis_job(
    transaction_schemas: List[TransactionSchema],
) -> AnalysisJobSchema:
    if not transaction_schemas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot start analysis with an empty transaction list.",
        )
    try:
        raw_transactions = [t.model_dump(mode="json") for t in transaction_schemas]
        task = run_analysis_task.delay(raw_transactions=raw_transactions)

        return AnalysisJobSchema(job_id=task.id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to queue analysis job: {e}",
        )


@router.get("/status/{job_id}", response_model=JobStatusSchema)
async def get_job_status(job_id: str) -> JobStatusSchema:
    """
    Consulta el estado de un trabajo de análisis en la cola de Celery.
    Cumple con RF-05b.
    """
    try:
        task_result = AsyncResult(job_id, app=celery_app)

        return JobStatusSchema(job_id=job_id, status=task_result.status)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking job status: {e}",
        )


@router.get(
    "/results/{job_id}",
    response_model=AnalysisReportSchema,
)
async def get_job_results(
    job_id: str,
    repo: ReportRepositoryPort = Depends(get_report_repository),
) -> AnalysisReportSchema:
    try:
        report = repo.get_by_job_id(job_id)

        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis report not found. The job may "
                "still be processing or the ID is invalid.",
            )

        return AnalysisReportSchema.model_validate(report)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving job results: {e}",
        )
