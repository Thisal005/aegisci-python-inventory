"""Inventory Movement ORM model."""

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aegisci_inventory.database import Base

if TYPE_CHECKING:
    from aegisci_inventory.models.item import Item


class MovementType(str, enum.Enum):
    """Enumeration of inventory movement types."""

    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"


class Movement(Base):
    """Inventory Stock Movement model."""

    __tablename__ = "movements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    movement_type: Mapped[MovementType] = mapped_column(
        Enum(MovementType), nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    item: Mapped["Item"] = relationship("Item", back_populates="movements")
