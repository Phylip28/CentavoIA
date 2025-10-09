from fastapi import APIRouter, HTTPException
from typing import List

from schemas.transaction_schema import Transaction

from models.analysis.analysis_service import AnalysisService
from views.analysis_view import AnalysisView

router = APIRouter()
analysis_service = AnalysisService()

@router.post("/analysis", status_code=200)
def perform_analysis(transactions: List[Transaction]):
    if not transactions:
        raise HTTPException(status_code=400, detail="Transactions list cannot be empty.")

    transactions_dict = [t.model_dump() for t in transactions]
    analysis_results = analysis_service.execute_analysis(transactions_dict)
    
    return AnalysisView.render_json(analysis_results)