"""Item ORM model."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aegisci_inventory.database import Base

if TYPE_CHECKING:
    from aegisci_inventory.models.category import Category
    from aegisci_inventory.models.movement import Movement


class Item(Base):
    """Inventory Item model."""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    quantity_in_stock: Mapped[int] = mapped_column(nullable=False, default=0)
    reorder_level: Mapped[int] = mapped_column(nullable=False, default=10)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    category: Mapped["Category | None"] = relationship("Category", back_populates="items")
    movements: Mapped[list["Movement"]] = relationship("Movement", back_populates="item", cascade="all, delete-orphan")
