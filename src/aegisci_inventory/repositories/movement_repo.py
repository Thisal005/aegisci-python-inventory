"""Movement repository implementation."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aegisci_inventory.models.movement import Movement
from aegisci_inventory.repositories.base import BaseRepository


class MovementRepository(BaseRepository[Movement]):
    """Repository handling inventory stock Movement DB operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with Movement model."""
        super().__init__(Movement, session)

    async def get_by_item_id(
        self, item_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Movement]:
        """Fetch stock movements for a specific item ordered by most recent."""
        result = await self.session.execute(
            select(Movement)
            .where(Movement.item_id == item_id)
            .order_by(Movement.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
