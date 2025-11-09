from datetime import date

from app.domain.analysis.analysis_models import Transaction
from app.domain.analysis.analysis_strategies import (
    AntSpendingStrategy,
    PeakSpendingStrategy,
)


def test_ant_spending_strategy_calculates_correctly():
    """
    Unit test (RNF-06) for RF-04 logic.
    Verifies that the ant spending strategy:
    1. Correctly sums the total.
    2. Correctly groups by category.
    3. Ignores expenses above the threshold.
    """
    # Arrange: Create test data with mixed amounts
    transactions = [
        Transaction("t1", 15.0, date(2025, 1, 1), "Coffee", "u1"),
        Transaction(
            "t2", 100.0, date(2025, 1, 1), "Restaurant", "u1"
        ),  # Above threshold
        Transaction("t3", 25.0, date(2025, 1, 2), "Coffee", "u1"),
        Transaction("t4", 30.0, date(2025, 1, 3), "Transport", "u1"),
    ]

    strategy = AntSpendingStrategy(ant_threshold=40.0)

    # Act: Execute strategy analysis
    strategy_name, results = strategy.analyze(transactions)

    # Assert: Verify calculations are exact
    assert strategy_name == "ant_spending"
    assert results["total_spent"] == 70.0  # 15 + 25 + 30
    assert results["by_category"] == {
        "Coffee": 40.0,  # 15 + 25
        "Transport": 30.0,
    }
    assert "Restaurant" not in results["by_category"]  # Excluded (above threshold)


def test_peak_spending_strategy_finds_peaks_correctly():
    """
    Unit test (RNF-06) for RF-03 logic.
    Verifies that the peak spending strategy:
    1. Groups transactions correctly by day.
    2. Identifies days that exceed the threshold.
    3. Ignores days below the threshold.
    """
    # Arrange: Create transactions across multiple days
    transactions = [
        # Day 1: Total = 180.0 (exceeds threshold of 150)
        Transaction("t1", 100.0, date(2025, 1, 1), "Restaurant", "u1"),
        Transaction("t2", 80.0, date(2025, 1, 1), "Supermarket", "u1"),
        # Day 2: Total = 120.0 (below threshold)
        Transaction("t3", 120.0, date(2025, 1, 2), "Transport", "u1"),
        # Day 3: Total = 200.0 (exceeds threshold)
        Transaction("t4", 200.0, date(2025, 1, 3), "Electronics", "u1"),
    ]

    strategy = PeakSpendingStrategy(peak_threshold=150.0)

    # Act: Execute peak detection
    strategy_name, results = strategy.analyze(transactions)

    # Assert: Verify peak detection accuracy
    assert strategy_name == "peak_spending"
    assert results["peak_days_found"] == 2

    # Verify first peak (Day 1)
    assert results["peaks"][0]["date"] == "2025-01-01"
    assert results["peaks"][0]["total_spent"] == 180.0

    # Verify second peak (Day 3)
    assert results["peaks"][1]["date"] == "2025-01-03"
    assert results["peaks"][1]["total_spent"] == 200.0
