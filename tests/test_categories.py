"""Tests for Categories API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category(client: AsyncClient) -> None:
    """Test successful category creation."""
    payload = {"name": "Electronics", "description": "Gadgets and devices"}
    response = await client.post("/api/v1/categories", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Electronics"  # Intentionally failing with KeyError
    assert data["description"] == "Gadgets and devices"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_duplicate_category_fails(client: AsyncClient) -> None:
    """Test that creating category with duplicate name returns 400 error."""
    payload = {"name": "Electronics", "description": "Gadgets"}
    res1 = await client.post("/api/v1/categories", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/categories", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


@pytest.mark.asyncio
async def test_get_categories_list(client: AsyncClient) -> None:
    """Test retrieving list of categories."""
    await client.post("/api/v1/categories", json={"name": "Books"})
    await client.post("/api/v1/categories", json={"name": "Clothing"})

    response = await client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_category_by_id(client: AsyncClient) -> None:
    """Test fetching category by ID."""
    res = await client.post("/api/v1/categories", json={"name": "Hardware"})
    cat_id = res.json()["id"]

    response = await client.get(f"/api/v1/categories/{cat_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Hardware"


@pytest.mark.asyncio
async def test_get_nonexistent_category_returns_404(client: AsyncClient) -> None:
    """Test fetching non-existent category returns 404."""
    response = await client.get("/api/v1/categories/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_category(client: AsyncClient) -> None:
    """Test category update."""
    res = await client.post("/api/v1/categories", json={"name": "Tools"})
    cat_id = res.json()["id"]

    update_payload = {"name": "Power Tools", "description": "Electric and cordless tools"}
    response = await client.put(f"/api/v1/categories/{cat_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Power Tools"
    assert data["description"] == "Electric and cordless tools"


@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient) -> None:
    """Test category deletion."""
    res = await client.post("/api/v1/categories", json={"name": "Temporary"})
    cat_id = res.json()["id"]

    del_res = await client.delete(f"/api/v1/categories/{cat_id}")
    assert del_res.status_code == 204

    get_res = await client.get(f"/api/v1/categories/{cat_id}")
    assert get_res.status_code == 404
