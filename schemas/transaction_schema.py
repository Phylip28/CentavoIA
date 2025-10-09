from pydantic import BaseModel, Field

class Transaction(BaseModel):
    id_transaction: str
    amount: float = Field(gt=0, description="Amount must be positive")
    date: str
    category: str
    user_id: str