from fastapi import APIRouter

from .dashboard import router as dashboard_router
from .user import router as user_router


api_router = APIRouter()

api_router.include_router(dashboard_router, prefix="/dashboard")
api_router.include_router(user_router, prefix="/user")
