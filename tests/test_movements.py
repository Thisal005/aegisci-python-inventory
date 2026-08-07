"""Tests for Stock Movements API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_record_movement_in(client: AsyncClient) -> None:
    """Test recording stock IN movement increases stock count."""
    item_res = await client.post(
        "/api/v1/items",
        json={"sku": "STOCK-IN-01", "name": "Test Item IN", "quantity_in_stock": 10},
    )
    item_id = item_res.json()["id"]

    movement_payload = {
        "item_id": item_id,
        "movement_type": "IN",
        "quantity": 15,
        "reason": "Restock shipment received",
    }
    response = await client.post("/api/v1/movements", json=movement_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["movement_type"] == "IN"
    assert data["quantity"] == 15

    # Check item quantity updated to 25
    item_updated = await client.get(f"/api/v1/items/{item_id}")
    assert item_updated.json()["quantity_in_stock"] == 25


@pytest.mark.asyncio
async def test_record_movement_out_success(client: AsyncClient) -> None:
    """Test recording stock OUT movement reduces stock count."""
    item_res = await client.post(
        "/api/v1/items",
        json={"sku": "STOCK-OUT-01", "name": "Test Item OUT", "quantity_in_stock": 20},
    )
    item_id = item_res.json()["id"]

    movement_payload = {
        "item_id": item_id,
        "movement_type": "OUT",
        "quantity": 8,
        "reason": "Customer order dispatched",
    }
    response = await client.post("/api/v1/movements", json=movement_payload)
    assert response.status_code == 201

    item_updated = await client.get(f"/api/v1/items/{item_id}")
    assert item_updated.json()["quantity_in_stock"] == 12


@pytest.mark.asyncio
async def test_record_movement_out_insufficient_stock_fails(client: AsyncClient) -> None:
    """Test recording stock OUT movement exceeding available stock returns 400."""
    item_res = await client.post(
        "/api/v1/items",
        json={"sku": "STOCK-LOW-01", "name": "Low Stock Item", "quantity_in_stock": 5},
    )
    item_id = item_res.json()["id"]

    movement_payload = {
        "item_id": item_id,
        "movement_type": "OUT",
        "quantity": 10,
        "reason": "Order request",
    }
    response = await client.post("/api/v1/movements", json=movement_payload)
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


@pytest.mark.asyncio
async def test_record_movement_adjustment(client: AsyncClient) -> None:
    """Test inventory stock count adjustment."""
    item_res = await client.post(
        "/api/v1/items",
        json={"sku": "STOCK-ADJ-01", "name": "Audit Item", "quantity_in_stock": 100},
    )
    item_id = item_res.json()["id"]

    movement_payload = {
        "item_id": item_id,
        "movement_type": "ADJUSTMENT",
        "quantity": 42,
        "reason": "Annual warehouse audit count",
    }
    response = await client.post("/api/v1/movements", json=movement_payload)
    assert response.status_code == 201

    item_updated = await client.get(f"/api/v1/items/{item_id}")
    assert item_updated.json()["quantity_in_stock"] == 42


@pytest.mark.asyncio
async def test_get_item_movement_history(client: AsyncClient) -> None:
    """Test retrieving transaction history for an item."""
    item_res = await client.post(
        "/api/v1/items",
        json={"sku": "STOCK-HIST-01", "name": "History Item", "quantity_in_stock": 50},
    )
    item_id = item_res.json()["id"]

    await client.post(
        "/api/v1/movements",
        json={"item_id": item_id, "movement_type": "IN", "quantity": 10, "reason": "Batch 1"},
    )
    await client.post(
        "/api/v1/movements",
        json={"item_id": item_id, "movement_type": "OUT", "quantity": 5, "reason": "Sale 1"},
    )

    response = await client.get(f"/api/v1/movements/item/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
