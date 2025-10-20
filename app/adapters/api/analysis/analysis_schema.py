from pydantic import BaseModel
from datetime import date


class TransactionSchema(BaseModel):

    transaction_id: str
    amount: float
    date: date
    category: str
    user_id: str

    class Config:
        from_attributes = True
