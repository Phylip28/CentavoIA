from datetime import datetime, timezone

class AnalysisView:

    @staticmethod
    def render_json(analysis_results: dict) -> dict:
        response = {
            "status": "success",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data": analysis_results
        }
        return response