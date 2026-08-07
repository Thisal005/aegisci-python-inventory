"""Health and readiness check API router."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from aegisci_inventory.config import Settings, get_settings
from aegisci_inventory.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check status response."""

    status: str
    app_name: str
    environment: str


class ReadinessResponse(BaseModel):
    """Readiness check status response."""

    status: str
    database: str


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Basic health check endpoint returning application info."""
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
    )


@router.get("/ready", response_model=ReadinessResponse, status_code=status.HTTP_200_OK)
async def readiness_check(db: AsyncSession = Depends(get_db)) -> ReadinessResponse:
    """Readiness check verifying database connectivity."""
    try:
        await db.execute(text("SELECT 1"))
        return ReadinessResponse(status="ready", database="connected")
    except Exception as exc:
        logger.error(f"Readiness check failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable",
        ) from exc
