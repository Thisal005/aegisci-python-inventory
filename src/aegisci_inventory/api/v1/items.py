"""Items API router."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from aegisci_inventory.database import get_db
from aegisci_inventory.repositories.category_repo import CategoryRepository
from aegisci_inventory.repositories.item_repo import ItemRepository
from aegisci_inventory.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from aegisci_inventory.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["Items"])


def get_item_service(db: AsyncSession = Depends(get_db)) -> ItemService:
    """Dependency provider for ItemService."""
    item_repo = ItemRepository(db)
    category_repo = CategoryRepository(db)
    return ItemService(item_repo, category_repo)


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create item",
)
async def create_item(
    data: ItemCreate,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """Create a new inventory item."""
    try:
        item = await service.create_item(data)
        item_with_relations = await service.get_item(item.id)
        assert item_with_relations is not None
        return service.to_response_dto(item_with_relations)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get(
    "",
    response_model=list[ItemResponse],
    status_code=status.HTTP_200_OK,
    summary="List items",
)
async def list_items(
    category_id: int | None = Query(None, description="Filter by category ID"),
    low_stock_only: bool = Query(False, description="Filter items at or below reorder level"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: ItemService = Depends(get_item_service),
) -> list[ItemResponse]:
    """Retrieve items with optional category or low stock filtering."""
    items = await service.get_items(
        category_id=category_id,
        low_stock_only=low_stock_only,
        skip=skip,
        limit=limit,
    )
    return [service.to_response_dto(item) for item in items]


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Get item by ID",
)
async def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """Get item details by ID."""
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return service.to_response_dto(item)


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Update item",
)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """Update inventory item properties."""
    try:
        await service.update_item(item_id, data)
        item_updated = await service.get_item(item_id)
        assert item_updated is not None
        return service.to_response_dto(item_updated)
    except ValueError as exc:
        if "not found" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete item",
)
async def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service),
) -> None:
    """Delete an item by ID."""
    try:
        await service.delete_item(item_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
