"""Item repository implementation."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from aegisci_inventory.models.item import Item
from aegisci_inventory.repositories.base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    """Repository handling Item DB operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with Item model."""
        super().__init__(Item, session)

    async def get_by_id_with_relations(self, item_id: int) -> Item | None:
        """Fetch item by ID loading category relation."""
        result = await self.session.execute(
            select(Item).options(selectinload(Item.category)).where(Item.id == item_id)
        )
        return result.scalar_one_or_none()

    async def get_by_sku(self, sku: str) -> Item | None:
        """Find item by unique SKU."""
        result = await self.session.execute(
            select(Item).options(selectinload(Item.category)).where(Item.sku == sku)
        )
        return result.scalar_one_or_none()

    async def search_items(
        self,
        category_id: int | None = None,
        low_stock_only: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Item]:
        """Query items with category/low-stock filters."""
        query = select(Item).options(selectinload(Item.category))

        if category_id is not None:
            query = query.where(Item.category_id == category_id)

        if low_stock_only:
            query = query.where(Item.quantity_in_stock <= Item.reorder_level)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
