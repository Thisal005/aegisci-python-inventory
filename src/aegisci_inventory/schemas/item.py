"""Item Pydantic schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from aegisci_inventory.schemas.category import CategoryResponse


class ItemBase(BaseModel):
    """Base item properties."""

    sku: str = Field(..., min_length=2, max_length=50, description="Stock Keeping Unit")
    name: str = Field(..., min_length=1, max_length=200, description="Item name")
    description: str | None = Field(None, max_length=1000, description="Item description")
    category_id: int | None = Field(None, description="Associated Category ID")
    unit_price: Decimal = Field(default=Decimal("0.00"), ge=0, description="Unit price")
    quantity_in_stock: int = Field(default=0, ge=0, description="Quantity in stock")
    reorder_level: int = Field(default=10, ge=0, description="Minimum stock before reorder")


class ItemCreate(ItemBase):
    """Item creation schema."""

    pass


class ItemUpdate(BaseModel):
    """Item update schema."""

    sku: str | None = Field(None, min_length=2, max_length=50)
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    category_id: int | None = None
    unit_price: Decimal | None = Field(None, ge=0)
    quantity_in_stock: int | None = Field(None, ge=0)
    reorder_level: int | None = Field(None, ge=0)


class ItemResponse(ItemBase):
    """Item response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryResponse | None = None
    is_low_stock: bool = Field(default=False, description="Flag indicating stock <= reorder_level")
