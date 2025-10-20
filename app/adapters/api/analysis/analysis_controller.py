from fastapi import APIRouter, Depends, HTTPException
from app.domain.analysis.analysis_ports import AnalysisServicePort
from app.domain.analysis.analysis_models import AnalysisReport, Transaction
from app.adapters.api.analysis.analysis_schema import TransactionSchema
from typing import List

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


def get_analysis_service() -> AnalysisServicePort:
    raise NotImplementedError("Dependency not injected")


@router.post("/", response_model=AnalysisReport)
async def run_analysis(
    transaction_schemas: List[TransactionSchema],
    service: AnalysisServicePort = Depends(get_analysis_service)
) -> AnalysisReport:

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

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing data: {e}")

    report = service.analyze_transactions(transactions)

    return report
