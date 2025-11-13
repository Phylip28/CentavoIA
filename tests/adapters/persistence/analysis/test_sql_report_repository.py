from sqlalchemy.orm import Session

from app.adapters.persistence.analysis.report_model import ReportModel
from app.adapters.persistence.analysis.sql_report_repository import (
    SQLAlchemyReportRepository,
)
from app.domain.analysis.analysis_models import AnalysisReport


def test_repository_can_save_report(db_session: Session):
    """
    Integration test (RNF-06) for the persistence adapter.
    Verifies that the repository saves and retrieves a report
    from a real Postgres database.

    'db_session' is the fixture we created in conftest.py
    """

    # Arrange: Create repository with test session
    def session_factory() -> Session:
        return db_session

    repository = SQLAlchemyReportRepository(session_factory=session_factory)

    report_domain = AnalysisReport(
        user_id="test_user_123",
        total_transactions=10,
        total_spent=500.75,
        strategy_results={"ant_spending": {"total_spent": 50.0}},
    )

    # Act: Save the report
    repository.save(report_domain)

    # Assert: Verify the data was saved correctly
    # Use the same session to query the database
    saved_report = (
        db_session.query(ReportModel).filter_by(user_id="test_user_123").first()
    )

    assert saved_report is not None
    assert saved_report.user_id == "test_user_123"
    assert saved_report.total_spent == 500.75
    assert saved_report.strategy_results["ant_spending"]["total_spent"] == 50.0
