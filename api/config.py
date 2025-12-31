from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from .models import ConfigResponse
from version import API_VERSION

router = APIRouter(prefix="/api", tags=["Configuration"])


class VersionInfo(BaseModel):
    """Version information for both API and frontend."""

    api_version: str
    frontend_version: Optional[str] = None


def create_config_router(app_config: dict):
    """Create config router with config dependency.

    Factory function that creates an APIRouter for configuration endpoints.
    Provides access to application configuration and version information.

    Args:
        app_config (dict): Application configuration dictionary.

    Returns:
        APIRouter: Configured router with config and version endpoints.
    """

    @router.get(
        "/config",
        response_model=ConfigResponse,
        status_code=200,
        summary="Get application configuration",
        description="Get application configuration settings",
    )
    def get_config():
        """Get application configuration.

        Returns application configuration settings including site title,
        degraded thresholds, and footer text.

        Returns:
            ConfigResponse: Response containing configuration dictionary.
        """
        return {"configuration": app_config}

    @router.get(
        "/versions",
        response_model=VersionInfo,
        status_code=200,
        summary="Get version information",
        description="Get API and frontend version information",
    )
    def get_versions():
        """Get version information.

        Returns the current versions of both the API and frontend by reading
        the frontend package.json file.

        Returns:
            VersionInfo: Response containing API and frontend version numbers.
        """
        import json
        import os

        frontend_version = "1.0.0"
        try:
            package_json_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "frontend", "package.json"
            )
            if os.path.exists(package_json_path):
                with open(package_json_path, "r") as f:
                    package_data = json.load(f)
                    frontend_version = package_data.get("version", "1.0.0")
        except Exception:
            pass

        return {"api_version": API_VERSION, "frontend_version": frontend_version}

    return router
