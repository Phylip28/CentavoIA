import logging
from datetime import date
from typing import Any, Dict, List

from app.core.celery_app import celery_app
from app.core.dependencies import create_analysis_service
from app.domain.analysis.analysis_models import Transaction
from app.domain.analysis.analysis_ports import AnalysisServicePort

logger = logging.getLogger(__name__)


@celery_app.task(name="run_analysis_task")
def run_analysis_task(raw_transactions: List[Dict[str, Any]]):
    """
    Asynchronous Celery task that runs analysis in the background.

    Receives serializable JSON data (dicts) and performs transaction analysis.
    """
    logger.info(
        f"Celery worker: Received task to analyze {len(raw_transactions)} transactions."
    )

    try:
        service: AnalysisServicePort = create_analysis_service()

        transactions: List[Transaction] = []
        for t_data in raw_transactions:
            t_data["date"] = date.fromisoformat(t_data["date"])
            transactions.append(Transaction(**t_data))

        service.analyze_transactions(transactions)

        logger.info(
            f"Celery worker: Task completed for user {transactions[0].user_id}."
        )
        return {"status": "success", "transactions_processed": len(transactions)}

    except Exception as e:
        logger.error(f"Celery worker: Analysis task failed. Error: {e}")
        raise e
