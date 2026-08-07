"""Item service handling business logic."""

from collections.abc import Sequence

from aegisci_inventory.models.item import Item
from aegisci_inventory.repositories.category_repo import CategoryRepository
from aegisci_inventory.repositories.item_repo import ItemRepository
from aegisci_inventory.schemas.item import ItemCreate, ItemResponse, ItemUpdate


class ItemService:
    """Service encapsulating business operations for Items."""

    def __init__(self, item_repo: ItemRepository, category_repo: CategoryRepository) -> None:
        """Initialize service with Item and Category repositories."""
        self.item_repo = item_repo
        self.category_repo = category_repo

    async def create_item(self, data: ItemCreate) -> Item:
        """Create a new item, validating SKU uniqueness and category reference."""
        existing_sku = await self.item_repo.get_by_sku(data.sku)
        if existing_sku:
            raise ValueError(f"Item with SKU '{data.sku}' already exists.")

        if data.category_id is not None:
            category = await self.category_repo.get_by_id(data.category_id)
            if not category:
                raise ValueError(f"Category with ID {data.category_id} not found.")

        item = Item(
            sku=data.sku,
            name=data.name,
            description=data.description,
            category_id=data.category_id,
            unit_price=data.unit_price,
            quantity_in_stock=data.quantity_in_stock,
            reorder_level=data.reorder_level,
        )
        return await self.item_repo.create(item)

    async def get_item(self, item_id: int) -> Item | None:
        """Fetch item by ID with relations loaded."""
        return await self.item_repo.get_by_id_with_relations(item_id)

    async def get_items(
        self,
        category_id: int | None = None,
        low_stock_only: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Item]:
        """Fetch list of items with optional filters."""
        return await self.item_repo.search_items(
            category_id=category_id,
            low_stock_only=low_stock_only,
            skip=skip,
            limit=limit,
        )

    async def _validate_update_fields(self, item: Item, data: ItemUpdate) -> None:
        """Validate SKU and Category ID updates."""
        if data.sku is not None and data.sku != item.sku:
            existing_sku = await self.item_repo.get_by_sku(data.sku)
            if existing_sku:
                raise ValueError(f"Item with SKU '{data.sku}' already exists.")
            item.sku = data.sku

        if data.category_id is not None and data.category_id != item.category_id:
            category = await self.category_repo.get_by_id(data.category_id)
            if not category:
                raise ValueError(f"Category with ID {data.category_id} not found.")
            item.category_id = data.category_id

    async def update_item(self, item_id: int, data: ItemUpdate) -> Item:
        """Update item details."""
        item = await self.item_repo.get_by_id_with_relations(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found.")

        await self._validate_update_fields(item, data)

        if data.name is not None:
            item.name = data.name
        if data.description is not None:
            item.description = data.description
        if data.unit_price is not None:
            item.unit_price = data.unit_price
        if data.quantity_in_stock is not None:
            item.quantity_in_stock = data.quantity_in_stock
        if data.reorder_level is not None:
            item.reorder_level = data.reorder_level

        return await self.item_repo.update(item)

    async def delete_item(self, item_id: int) -> None:
        """Delete item by ID."""
        item = await self.item_repo.get_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found.")
        await self.item_repo.delete(item)

    @staticmethod
    def to_response_dto(item: Item) -> ItemResponse:
        """Convert Item ORM model to response DTO including calculated fields."""
        return ItemResponse(
            id=item.id,
            sku=item.sku,
            name=item.name,
            description=item.description,
            category_id=item.category_id,
            unit_price=item.unit_price,
            quantity_in_stock=item.quantity_in_stock,
            reorder_level=item.reorder_level,
            created_at=item.created_at,
            updated_at=item.updated_at,
            category=item.category,  # type: ignore[arg-type]
            is_low_stock=item.quantity_in_stock <= item.reorder_level,
        )
