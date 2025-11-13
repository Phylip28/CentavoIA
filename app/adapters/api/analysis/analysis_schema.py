from datetime import date
from typing import Any, Dict

from pydantic import BaseModel, Field


class TransactionSchema(BaseModel):
    transaction_id: str
    amount: float
    date: date
    category: str
    user_id: str

    class Config:
        from_attributes = True


class AnalysisReportSchema(BaseModel):
    user_id: str
    total_transactions: int
    total_spent: float
    strategy_results: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class AnalysisJobSchema(BaseModel):
    """
    Schema for the response of an initiated analysis job.
    Complies with RF-05a.
    """

    job_id: str
    status: str = "pending"
    message: str = "Analysis job successfully queued."


class JobStatusSchema(BaseModel):
    job_id: str
    status: str

    class Config:
        from_attributes = True
