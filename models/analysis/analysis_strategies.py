class SimplePeakDetectionStrategy:

    def __init__(self, threshold):
        if threshold <= 0:
            raise ValueError("Threshold must be a positive number.")
        
        self.threshold = threshold

    def find(self, transactions: list[dict]) -> list[dict]:
        daily_spend = {}

        for transaction in transactions:
            daily_spend[transaction['date']] = daily_spend.get(transaction['date'], 0) + transaction['amount']

        peaks = [
            {"date": date, "total": total}
            for date, total in daily_spend.items()
            if total > self.threshold
        ]

        return peaks