"""Categories API router."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from aegisci_inventory.database import get_db
from aegisci_inventory.repositories.category_repo import CategoryRepository
from aegisci_inventory.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from aegisci_inventory.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    """Dependency provider for CategoryService."""
    repo = CategoryRepository(db)
    return CategoryService(repo)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create category",
)
async def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    """Create a new product category."""
    try:
        category = await service.create_category(data)
        return CategoryResponse.model_validate(category)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get(
    "",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="List categories",
)
async def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: CategoryService = Depends(get_category_service),
) -> Sequence[CategoryResponse]:
    """Retrieve all categories with pagination."""
    categories = await service.get_all_categories(skip=skip, limit=limit)
    return [CategoryResponse.model_validate(c) for c in categories]


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get category by ID",
)
async def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    """Get category details by ID."""
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found",
        )
    return CategoryResponse.model_validate(category)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update category",
)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    """Update an existing category."""
    try:
        category = await service.update_category(category_id, data)
        return CategoryResponse.model_validate(category)
    except ValueError as exc:
        if "not found" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete category",
)
async def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
) -> None:
    """Delete a category by ID."""
    try:
        await service.delete_category(category_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
