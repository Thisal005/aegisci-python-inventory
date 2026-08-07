"""Inventory stock movement service."""

from collections.abc import Sequence

from aegisci_inventory.models.movement import Movement, MovementType
from aegisci_inventory.repositories.item_repo import ItemRepository
from aegisci_inventory.repositories.movement_repo import MovementRepository
from aegisci_inventory.schemas.movement import MovementCreate


class InventoryService:
    """Service encapsulating stock movement and stock level adjustments."""

    def __init__(self, movement_repo: MovementRepository, item_repo: ItemRepository) -> None:
        """Initialize with Movement and Item repositories."""
        self.movement_repo = movement_repo
        self.item_repo = item_repo

    async def record_movement(self, data: MovementCreate) -> Movement:
        """Record inventory stock movement and adjust item stock quantity."""
        item = await self.item_repo.get_by_id(data.item_id)
        if not item:
            raise ValueError(f"Item with ID {data.item_id} not found.")

        if data.movement_type == MovementType.IN:
            item.quantity_in_stock += data.quantity
        elif data.movement_type == MovementType.OUT:
            if item.quantity_in_stock < data.quantity:
                raise ValueError(
                    f"Insufficient stock for SKU '{item.sku}'. Available: {item.quantity_in_stock}, requested: {data.quantity}."
                )
            item.quantity_in_stock -= data.quantity
        elif data.movement_type == MovementType.ADJUSTMENT:
            item.quantity_in_stock = data.quantity

        await self.item_repo.update(item)

        movement = Movement(
            item_id=data.item_id,
            movement_type=data.movement_type,
            quantity=data.quantity,
            reason=data.reason,
        )
        return await self.movement_repo.create(movement)

    async def get_movements_for_item(
        self, item_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Movement]:
        """Retrieve historical stock movements for an item."""
        item = await self.item_repo.get_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found.")

        return await self.movement_repo.get_by_item_id(item_id, skip=skip, limit=limit)
