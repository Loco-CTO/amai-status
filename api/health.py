from fastapi import APIRouter
from pydantic import BaseModel

from .models import HealthResponse
from version import API_VERSION

router = APIRouter(tags=["Health"])


class VersionResponse(BaseModel):
    """API version information."""

    api_version: str
    status: str = "ok"


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=200,
    summary="Health check",
    description="Check if the API service is running",
)
def health_check():
    """Health check endpoint.

    Simple endpoint to verify that the API service is running and responsive.

    Returns:
        HealthResponse: Health status response.
    """
    return {"status": "ok"}


@router.get(
    "/version",
    response_model=VersionResponse,
    status_code=200,
    summary="API version",
    description="Get API version information",
)
def get_version():
    """Get API version information.

    Returns the current version of the API.

    Returns:
        VersionResponse: API version information with status.
    """
    return {"api_version": API_VERSION, "status": "ok"}
