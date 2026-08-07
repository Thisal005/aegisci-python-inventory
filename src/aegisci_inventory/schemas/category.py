"""Category Pydantic schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    """Base category properties."""

    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: str | None = Field(None, max_length=500, description="Category description")


class CategoryCreate(CategoryBase):
    """Category creation schema."""

    pass


class CategoryUpdate(BaseModel):
    """Category update schema."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class CategoryResponse(CategoryBase):
    """Category response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
