"""Inventory Movements API router."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from aegisci_inventory.database import get_db
from aegisci_inventory.repositories.item_repo import ItemRepository
from aegisci_inventory.repositories.movement_repo import MovementRepository
from aegisci_inventory.schemas.movement import MovementCreate, MovementResponse
from aegisci_inventory.services.inventory_service import InventoryService

router = APIRouter(prefix="/movements", tags=["Stock Movements"])


def get_inventory_service(db: AsyncSession = Depends(get_db)) -> InventoryService:
    """Dependency provider for InventoryService."""
    movement_repo = MovementRepository(db)
    item_repo = ItemRepository(db)
    return InventoryService(movement_repo, item_repo)


@router.post(
    "",
    response_model=MovementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record stock movement",
)
async def record_movement(
    data: MovementCreate,
    service: InventoryService = Depends(get_inventory_service),
) -> MovementResponse:
    """Record a stock movement (IN, OUT, ADJUSTMENT) for an item."""
    try:
        movement = await service.record_movement(data)
        return MovementResponse.model_validate(movement)
    except ValueError as exc:
        if "not found" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get(
    "/item/{item_id}",
    response_model=list[MovementResponse],
    status_code=status.HTTP_200_OK,
    summary="Get movement history for item",
)
async def get_item_movements(
    item_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: InventoryService = Depends(get_inventory_service),
) -> Sequence[MovementResponse]:
    """Retrieve stock movement transaction logs for a given item."""
    try:
        movements = await service.get_movements_for_item(
            item_id=item_id, skip=skip, limit=limit
        )
        return [MovementResponse.model_validate(m) for m in movements]
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
