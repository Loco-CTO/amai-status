from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(tags=["Assets"])


def create_assets_router():
    """Create assets router for static file serving.

    Factory function that creates an APIRouter for asset endpoints.
    Provides access to static assets like logos and images.

    Returns:
        APIRouter: Configured router with asset endpoints.
    """

    @router.get(
        "/logo.png",
        status_code=200,
        summary="Get logo image",
        description="Get the site logo image",
    )
    def get_logo():
        """Get logo image.

        Returns the PNG logo image file for the status page.
        Response is cached for 7 days (604800 seconds).

        Returns:
            FileResponse: Logo image as PNG file with cache headers.
        """
        logo_path = os.path.join(os.path.dirname(__file__), "..", "public", "logo.png")

        if not os.path.exists(logo_path):
            raise FileNotFoundError("Logo file not found")

        return FileResponse(
            logo_path,
            media_type="image/png",
            headers={"Cache-Control": "public, max-age=604800"},
        )

    return router
