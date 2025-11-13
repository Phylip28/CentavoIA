from sqlalchemy import JSON, Column, Float, Integer, String

from app.adapters.persistence.database import Base


class ReportModel(Base):
    __tablename__ = "analysis_reports"

    job_id = Column(String, primary_key=True)

    user_id = Column(String, nullable=False, index=True)
    total_transactions = Column(Integer, nullable=False)
    total_spent = Column(Float, nullable=False)

    strategy_results = Column(JSON, nullable=False)
