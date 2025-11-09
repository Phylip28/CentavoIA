from datetime import date

from app.domain.analysis.analysis_models import Transaction
from app.domain.analysis.analysis_strategies import AntSpendingStrategy


def test_ant_spending_strategy_calculates_correctly():
    """
    Unit test (RNF-06) for RF-04 logic.
    Verifies that the ant spending strategy:
    1. Correctly sums the total.
    2. Correctly groups by category.
    3. Ignores expenses above the threshold.
    """

    # Test data
    transactions = [
        Transaction("t1", 15.0, date(2025, 1, 1), "Coffee", "u1"),
        Transaction(
            "t2", 100.0, date(2025, 1, 1), "Restaurant", "u1"
        ),  # Should be ignored
        Transaction("t3", 25.0, date(2025, 1, 2), "Coffee", "u1"),
        Transaction("t4", 30.0, date(2025, 1, 3), "Transport", "u1"),
    ]

    # Create the strategy with a threshold of $40
    strategy = AntSpendingStrategy(ant_threshold=40.0)

    # Act
    strategy_name, results = strategy.analyze(transactions)

    # Assert
    # Verify that calculations are exact
    assert strategy_name == "ant_spending"
    assert results["total_spent"] == 70.0
    assert results["by_category"] == {
        "Coffee": 40.0,
        "Transport": 30.0,
    }
    # Verify that 'Restaurant' was not included
    assert "Restaurant" not in results["by_category"]
