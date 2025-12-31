from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta

from .utils import aggregate_heartbeat_data
import database

router = APIRouter(prefix="/api/heartbeat", tags=["Status"])


def create_heartbeat_router(app_config: dict):
    """Create heartbeat router with config dependency.

    Factory function that creates an APIRouter for heartbeat endpoints.
    Provides aggregated heartbeat data for monitors at various time intervals.

    Args:
        app_config (dict): Application configuration containing degraded thresholds.

    Returns:
        APIRouter: Configured router with heartbeat endpoints.
    """

    @router.get(
        "",
        response_model=dict,
        status_code=200,
        summary="Get aggregated heartbeat data for a monitor",
        description="Get heartbeat data aggregated by time interval",
    )
    def get_aggregated_heartbeat(
        monitor_name: str, interval: str = "all", hours: int = 24
    ):
        """Get aggregated heartbeat data for a specific monitor.

        Aggregates heartbeat records by the specified time interval, providing
        a summary view of monitor performance over the requested period.

        Args:
            monitor_name (str): Name of the monitor to query.
            interval (str): Time interval ('all', 'hour', 'day', 'week'). Default: 'all'.
            hours (int): Number of hours to look back (default: 24).

        Returns:
            dict: Dictionary with monitor_name, interval, and aggregated heartbeat data.

        Raises:
            HTTPException: 400 if invalid interval, 404 if monitor not found.
        """
        from .models import MonitorRecord

        valid_intervals = ["all", "hour", "day", "week"]
        if interval not in valid_intervals:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid interval. Must be one of: {', '.join(valid_intervals)}",
            )

        db = database.SessionLocal()
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            records = (
                db.query(MonitorRecord)
                .filter(
                    MonitorRecord.monitor_name == monitor_name,
                    MonitorRecord.timestamp >= cutoff_time,
                )
                .order_by(MonitorRecord.timestamp.asc())
                .all()
            )

            if not records:
                raise HTTPException(
                    status_code=404,
                    detail=f"Monitor '{monitor_name}' not found or no data available",
                )

            aggregated_data = aggregate_heartbeat_data(records, interval, app_config)

            return {
                "monitor_name": monitor_name,
                "interval": interval,
                "heartbeat": aggregated_data,
            }
        finally:
            db.close()

    return router
