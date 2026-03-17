from fastapi import APIRouter
from pydantic import BaseModel

from .models import ConfigResponse
from version import API_VERSION

router = APIRouter(prefix="/api", tags=["Configuration"])


class VersionInfo(BaseModel):
    """Version information for API."""

    api_version: str


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
        description="Get API version information",
    )
    def get_versions():
        """Get version information.

        Returns the current API version.

        Returns:
            VersionInfo: Response containing API version.
        """
        return {"api_version": API_VERSION}

    return router
