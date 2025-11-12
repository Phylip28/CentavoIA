from typing import List

from fastapi import APIRouter, HTTPException, status

from app.adapters.api.analysis.analysis_schema import (
    AnalysisJobSchema,
    TransactionSchema,
)
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
