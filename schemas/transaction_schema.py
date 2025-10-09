from pydantic import BaseModel, Field

class Transaction(BaseModel):
    id_transaccion: str
    monto: float = Field(gt=0, description="Amount must be positive")
    fecha: str
    categoría: str
    id_usuario: str