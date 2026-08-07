"""Base repository implementation using SQLAlchemy AsyncSession."""

from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aegisci_inventory.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD Async Repository."""

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        """Initialize repository with model class and session."""
        self.model = model
        self.session = session

    async def get_by_id(self, id_: int) -> ModelType | None:
        """Fetch entity by primary key ID."""
        model_id_attr = self.model.id  # type: ignore[attr-defined]
        result = await self.session.execute(
            select(self.model).where(model_id_attr == id_)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Fetch paginated list of entities."""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, instance: ModelType) -> ModelType:
        """Add new entity to session."""
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: ModelType) -> ModelType:
        """Commit modified entity."""
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        """Remove entity from session."""
        await self.session.delete(instance)
        await self.session.commit()
