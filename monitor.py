import asyncio
import logging
from datetime import datetime
from typing import Optional

import aiohttp

import database
from aggregation import upsert_aggregates_for_record
from api.models import MonitorRecord

logger = logging.getLogger(__name__)

monitor_last_status = {}


def _save_record(db, record: MonitorRecord, app_config: dict, monitor_name: str):
    """Persist a monitor record and keep session state clean on DB failures."""
    try:
        db.add(record)
        upsert_aggregates_for_record(db, record, app_config)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.exception(f"{monitor_name}: Failed to persist monitor record: {e}")


async def send_discord_notification(
    name: str,
    is_up: bool,
    status_code: Optional[int],
    response_time: Optional[float],
    monitor: dict,
):
    """Send status change notification to Discord.

    Posts an embed message to the configured Discord webhook URL with
    monitor status information.

    Args:
        name (str): Name of the monitor.
        is_up (bool): Whether the monitor is up or down.
        status_code (Optional[int]): HTTP status code, None if error/timeout.
        response_time (Optional[float]): Response time in seconds, None if error/timeout.
        monitor (dict): Monitor configuration containing Discord webhook URL.
    """
    webhook_url = monitor.get("discordIntegration", {}).get("webhookUrl")
    if not webhook_url:
        return

    status_text = "✅ UP" if is_up else "❌ DOWN"
    color = 3066993 if is_up else 15158332

    embed = {
        "title": f"{name} - {status_text}",
        "color": color,
        "fields": [
            {"name": "URL", "value": monitor["url"], "inline": False},
            {
                "name": "Status Code",
                "value": str(status_code) if status_code else "N/A",
                "inline": True,
            },
            {
                "name": "Response Time",
                "value": f"{response_time:.2f}s" if response_time else "N/A",
                "inline": True,
            },
            {"name": "Timestamp", "value": datetime.now().isoformat(), "inline": False},
        ],
    }

    try:
        async with (
            aiohttp.ClientSession() as session,
            session.post(webhook_url, json={"embeds": [embed]}) as response,
        ):
            if response.status not in [200, 204]:
                logger.warning(f"Discord webhook failed for {name}: {response.status}")
    except Exception as e:
        logger.error(f"Failed to send Discord notification: {str(e)}")


async def check_monitor(
    monitor: dict, session: aiohttp.ClientSession, app_config: dict
):
    """Check a single monitor's status and record results.

    Makes an HTTP request to the monitor URL, records the result to the database,
    and sends Discord notifications if the status changes.

    Args:
        monitor (dict): Monitor configuration with URL and settings.
        session (aiohttp.ClientSession): HTTP session for making requests.
        app_config (dict): Application configuration.
    """
    name = monitor["name"]
    url = monitor["url"]
    accepted_codes = set(monitor.get("accepted_status_codes", [200]))
    verify_ssl = monitor.get("verify", True)
    db = database.SessionLocal()

    try:
        start_time = datetime.now()
        async with session.get(
            url, ssl=verify_ssl, timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            status_code = response.status
            is_up = status_code in accepted_codes

            record = MonitorRecord(
                monitor_name=name,
                timestamp=end_time,
                status_code=status_code,
                is_up=is_up,
                response_time=response_time,
            )
            _save_record(db, record, app_config, name)
            logger.info(
                f"{name}: {status_code} ({response_time:.2f}s) - {'UP' if is_up else 'DOWN'}"
            )

            last_status = monitor_last_status.get(name)
            monitor_last_status[name] = is_up

            if monitor.get("discordIntegration", {}).get("webhookUrl") and (
                last_status is None or last_status != is_up
            ):
                await send_discord_notification(
                    name, is_up, status_code, response_time, monitor
                )

    except asyncio.TimeoutError:
        record = MonitorRecord(
            monitor_name=name,
            timestamp=datetime.now(),
            status_code=None,
            is_up=False,
            response_time=None,
        )
        _save_record(db, record, app_config, name)
        logger.warning(f"{name}: TIMEOUT - DOWN")

        last_status = monitor_last_status.get(name)
        monitor_last_status[name] = False

        if monitor.get("discordIntegration", {}).get("webhookUrl") and (
            last_status is None or last_status is not False
        ):
            await send_discord_notification(name, False, None, None, monitor)
    except Exception as e:
        record = MonitorRecord(
            monitor_name=name,
            timestamp=datetime.now(),
            status_code=None,
            is_up=False,
            response_time=None,
        )
        _save_record(db, record, app_config, name)

        logger.error(f"{name}: ERROR - {str(e)}")

        last_status = monitor_last_status.get(name)
        monitor_last_status[name] = False

        if monitor.get("discordIntegration", {}).get("webhookUrl") and (
            last_status is None or last_status is not False
        ):
            await send_discord_notification(name, False, None, None, monitor)
    finally:
        db.close()


async def monitor_service(monitors_config: list, app_config: dict):
    """Main monitoring service loop.

    Continuously checks all configured monitors at their configured intervals
    and records their status. Runs in a background task for the lifetime of
    the application.

    Args:
        monitors_config (list): List of monitor configurations.
    """
    await asyncio.sleep(2)

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                tasks = []
                for monitor in monitors_config:
                    tasks.append(check_monitor(monitor, session, app_config))

                if tasks:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    for result in results:
                        if isinstance(result, Exception):
                            logger.error(
                                "Unexpected monitor task exception that was recovered: %s",
                                result,
                                exc_info=(
                                    type(result),
                                    result,
                                    result.__traceback__,
                                ),
                            )

                interval_ms = (
                    monitors_config[0].get("interval", 30000)
                    if monitors_config
                    else 30000
                )
                if not isinstance(interval_ms, (int, float)) or interval_ms <= 0:
                    logger.warning(
                        f"Invalid monitor interval '{interval_ms}', using default 30000ms"
                    )
                    interval_ms = 30000
                await asyncio.sleep(interval_ms / 1000)
            except Exception as e:
                logger.exception(f"Monitor service loop recovered from error: {e}")
                await asyncio.sleep(1)
