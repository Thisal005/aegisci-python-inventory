"""Inventory Movement Pydantic schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from aegisci_inventory.models.movement import MovementType


class MovementCreate(BaseModel):
    """Movement creation request schema."""

    item_id: int = Field(..., description="Target Item ID")
    movement_type: MovementType = Field(..., description="Type of stock movement (IN, OUT, ADJUSTMENT)")
    quantity: int = Field(..., description="Quantity added, removed, or set")
    reason: str | None = Field(None, max_length=255, description="Reason for stock movement")

    @model_validator(mode="after")
    def validate_quantity(self) -> "MovementCreate":
        """Validate quantity according to movement type."""
        if self.movement_type in (MovementType.IN, MovementType.OUT) and self.quantity <= 0:
            raise ValueError("Quantity must be strictly positive (> 0) for IN and OUT movements.")
        if self.movement_type == MovementType.ADJUSTMENT and self.quantity < 0:
            raise ValueError("Quantity must be non-negative (>= 0) for ADJUSTMENT movements.")
        return self


class MovementResponse(BaseModel):
    """Movement response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    movement_type: MovementType
    quantity: int
    reason: str | None = None
    created_at: datetime
