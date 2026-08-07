"""Tests for health and readiness endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient) -> None:
    """Test root metadata endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """Test /api/v1/health endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data


@pytest.mark.asyncio
async def test_readiness_check(client: AsyncClient) -> None:
    """Test /api/v1/ready endpoint."""
    response = await client.get("/api/v1/ready")
    assert response.status_code == 500  # Intentionally failing
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"
