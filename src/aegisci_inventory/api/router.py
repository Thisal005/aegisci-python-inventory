"""Main API router including versioned endpoints."""

from fastapi import APIRouter

from aegisci_inventory.api.v1 import v1_router

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
