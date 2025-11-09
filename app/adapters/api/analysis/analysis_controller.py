from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.adapters.api.analysis.analysis_schema import (
    AnalysisReportSchema,
    TransactionSchema,
)
from app.domain.analysis.analysis_models import EmptyTransactionListError, Transaction
from app.domain.analysis.analysis_ports import AnalysisServicePort

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


def get_analysis_service() -> AnalysisServicePort:
    raise NotImplementedError("Dependency not injected")


@router.post("/", response_model=AnalysisReportSchema)
async def run_analysis(
    transaction_schemas: List[TransactionSchema],
    service: AnalysisServicePort = Depends(get_analysis_service)
) -> AnalysisReportSchema:

    try:
        transactions: List[Transaction] = [
            Transaction(
                transaction_id=t.transaction_id,
                amount=t.amount,
                date=t.date,
                category=t.category,
                user_id=t.user_id
            )
            for t in transaction_schemas
        ]

        report = service.analyze_transactions(transactions)
    except EmptyTransactionListError:
        raise HTTPException(
            status_code=400, detail="The transaction list is empty."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        )

    return AnalysisReportSchema.model_validate(report)
