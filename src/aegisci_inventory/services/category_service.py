"""Category service handling business logic."""

from collections.abc import Sequence

from aegisci_inventory.models.category import Category
from aegisci_inventory.repositories.category_repo import CategoryRepository
from aegisci_inventory.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """Service encapsulating business operations for Categories."""

    def __init__(self, repo: CategoryRepository) -> None:
        """Initialize service with Category repository."""
        self.repo = repo

    async def create_category(self, data: CategoryCreate) -> Category:
        """Create a new category, ensuring unique name."""
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise ValueError(f"Category with name '{data.name}' already exists.")

        category = Category(name=data.name, description=data.description)
        return await self.repo.create(category)

    async def get_category(self, category_id: int) -> Category | None:
        """Fetch category by ID."""
        return await self.repo.get_by_id(category_id)

    async def get_all_categories(
        self, skip: int = 0, limit: int = 100
    ) -> Sequence[Category]:
        """Fetch all categories."""
        return await self.repo.get_all(skip=skip, limit=limit)

    async def update_category(
        self, category_id: int, data: CategoryUpdate
    ) -> Category:
        """Update category properties."""
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found.")

        if data.name is not None and data.name != category.name:
            existing = await self.repo.get_by_name(data.name)
            if existing:
                raise ValueError(f"Category with name '{data.name}' already exists.")
            category.name = data.name

        if data.description is not None:
            category.description = data.description

        return await self.repo.update(category)

    async def delete_category(self, category_id: int) -> None:
        """Delete category by ID."""
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found.")
        await self.repo.delete(category)
