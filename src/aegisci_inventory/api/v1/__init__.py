"""API v1 router composition."""

from fastapi import APIRouter

from aegisci_inventory.api.v1.categories import router as categories_router
from aegisci_inventory.api.v1.health import router as health_router
from aegisci_inventory.api.v1.items import router as items_router
from aegisci_inventory.api.v1.movements import router as movements_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(health_router)
v1_router.include_router(categories_router)
v1_router.include_router(items_router)
v1_router.include_router(movements_router)
