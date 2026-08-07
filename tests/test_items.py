"""Tests for Items API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient) -> None:
    """Test successful item creation."""
    cat_res = await client.post("/api/v1/categories", json={"name": "Audio"})
    cat_id = cat_res.json()["id"]

    item_payload = {
        "sku": "HEADPHONE-001",
        "name": "Wireless Headphones",
        "description": "Noise cancelling headphones",
        "category_id": cat_id,
        "unit_price": "149.99",
        "quantity_in_stock": 25,
        "reorder_level": 5,
    }
    response = await client.post("/api/v1/items", json=item_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == "HEADPHONE-001"
    assert data["name"] == "Wireless Headphones"
    assert data["category"]["name"] == "Audio"
    assert data["is_low_stock"] is False


@pytest.mark.asyncio
async def test_create_item_duplicate_sku_fails(client: AsyncClient) -> None:
    """Test creating item with duplicate SKU returns 400."""
    payload = {"sku": "SKU-DUP", "name": "Item 1", "unit_price": "10.00"}
    res1 = await client.post("/api/v1/items", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/items", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


@pytest.mark.asyncio
async def test_create_item_invalid_category_fails(client: AsyncClient) -> None:
    """Test creating item with non-existent category returns 400."""
    payload = {"sku": "SKU-BAD-CAT", "name": "Item Bad Cat", "category_id": 99999}
    response = await client.post("/api/v1/items", json=payload)
    assert response.status_code == 400
    assert "Category with ID 99999 not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_list_items_with_low_stock_filter(client: AsyncClient) -> None:
    """Test low stock filtering."""
    # Item 1: Normal stock
    await client.post(
        "/api/v1/items",
        json={"sku": "SKU-NORMAL", "name": "Normal Stock", "quantity_in_stock": 50, "reorder_level": 10},
    )
    # Item 2: Low stock
    await client.post(
        "/api/v1/items",
        json={"sku": "SKU-LOW", "name": "Low Stock", "quantity_in_stock": 3, "reorder_level": 10},
    )

    res_all = await client.get("/api/v1/items")
    assert res_all.status_code == 200
    assert len(res_all.json()) == 2

    res_low = await client.get("/api/v1/items?low_stock_only=true")
    assert res_low.status_code == 200
    data_low = res_low.json()
    assert len(data_low) == 1
    assert data_low[0]["sku"] == "SKU-LOW"
    assert data_low[0]["is_low_stock"] is True


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient) -> None:
    """Test item update."""
    res = await client.post(
        "/api/v1/items",
        json={"sku": "SKU-ORIGINAL", "name": "Original Name", "unit_price": "5.00"},
    )
    item_id = res.json()["id"]

    update_payload = {"name": "Updated Name", "unit_price": "7.50"}
    upd_res = await client.put(f"/api/v1/items/{item_id}", json=update_payload)
    assert upd_res.status_code == 200
    data = upd_res.json()
    assert data["name"] == "Updated Name"
    assert data["unit_price"] == "7.50"


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient) -> None:
    """Test item deletion."""
    res = await client.post("/api/v1/items", json={"sku": "SKU-DEL", "name": "To Delete"})
    item_id = res.json()["id"]

    del_res = await client.delete(f"/api/v1/items/{item_id}")
    assert del_res.status_code == 204

    get_res = await client.get(f"/api/v1/items/{item_id}")
    assert get_res.status_code == 404
