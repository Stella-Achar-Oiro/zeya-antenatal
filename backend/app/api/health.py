"""Health check router.

GET /api/health — liveness probe for App Runner and load balancers.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response body for the health check endpoint.

    Args:
        status: Always 'ok' when the service is running.
        service: Human-readable service name.
    """

    status: str
    service: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Return service liveness status.

    Returns:
        HealthResponse with status 'ok'.
    """
    return HealthResponse(status="ok", service="zeya-antenatal")
