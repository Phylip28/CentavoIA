import uuid

from sqlalchemy import JSON, Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.adapters.persistence.database import Base


class ReportModel(Base):
    __tablename__ = "analysis_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(String, nullable=False, index=True)
    total_transactions = Column(Integer, nullable=False)
    total_spent = Column(Float, nullable=False)

    strategy_results = Column(JSON, nullable=False)
