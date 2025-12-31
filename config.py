import os
import logging
from typing import Tuple, Dict, List, Any

try:
    import yaml
except ImportError:
    yaml = None

logger = logging.getLogger(__name__)


def load_config() -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    """Load configuration from config.yaml.

    Parses the YAML configuration file and converts field names from snake_case to camelCase
    for API responses. Also converts snake_case monitor integration fields.

    Returns:
        tuple: A 3-tuple containing:
            - monitors_config (List[Dict]): List of monitor configurations
            - app_config (Dict): Application configuration settings
            - server_config (Dict): Server binding configuration

    Raises:
        FileNotFoundError: If config.yaml does not exist.
        ImportError: If PyYAML is not installed.
        ValueError: If the configuration file is empty.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file not found at {config_path}. "
            "Please copy config.example.yaml to config.yaml in the amai-status directory and customize it."
        )

    with open(config_path, "r", encoding="utf-8") as f:
        if yaml is None:
            raise ImportError(
                "PyYAML is required to parse config.yaml. Install it with: pip install pyyaml"
            )
        config = yaml.safe_load(f)

    if not config:
        raise ValueError("Configuration file is empty")

    monitors_config = config.get("monitors", [])

    for monitor in monitors_config:
        if "discord_integration" in monitor and "discordIntegration" not in monitor:
            discord_config = monitor.pop("discord_integration")
            monitor["discordIntegration"] = {
                "webhookUrl": discord_config.get("webhook_url", "")
            }

    app_config = config.get("configuration", {})

    converted_app_config = {}
    for key, value in app_config.items():
        if key == "footer_text":
            converted_app_config["footerText"] = value
        elif key == "site_title":
            converted_app_config["siteTitle"] = value
        elif key == "degraded_threshold":
            converted_app_config["degraded_threshold"] = value
        elif key == "degraded_percentage_threshold":
            converted_app_config["degraded_percentage_threshold"] = value
        else:
            converted_app_config[key] = value

    app_config = converted_app_config
    server_config = config.get("server", {})

    logger.info(f"Loaded {len(monitors_config)} monitors from config")
    logger.info(
        f"Server configured to bind to {server_config.get('host', '0.0.0.0')}:{server_config.get('port', 8182)}"
    )

    return monitors_config, app_config, server_config
