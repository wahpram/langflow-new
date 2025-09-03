from fastapi import APIRouter
from .health import router as health_router
from .emit import router as emit_router
from .org_search import router as org_search_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(emit_router)
api_router.include_router(org_search_router)