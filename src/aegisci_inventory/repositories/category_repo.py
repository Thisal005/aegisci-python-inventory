"""Category repository implementation."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aegisci_inventory.models.category import Category
from aegisci_inventory.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository handling Category DB operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with Category model."""
        super().__init__(Category, session)

    async def get_by_name(self, name: str) -> Category | None:
        """Find category by unique name."""
        result = await self.session.execute(
            select(Category).where(Category.name == name)
        )
        return result.scalar_one_or_none()
