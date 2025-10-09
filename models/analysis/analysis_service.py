from .analysis_strategies import SimplePeakDetectionStrategy

class AnalysisService:

    def __init__(self):
        self.strategies = [
            SimplePeakDetectionStrategy(threshold=150.0)
        ]

    def execute_analysis(self, transactions: list[dict]) -> dict:
        all_patterns = {}
        for strategy in self.strategies:
            patterns = strategy.find(transactions)

            all_patterns[strategy.__class__.__name__] = patterns

        return all_patterns