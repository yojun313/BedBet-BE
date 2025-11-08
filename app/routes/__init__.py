from .auth_routes import router as auth_router
from fastapi import APIRouter

try:
    from .team_routes import router as team_router 
except Exception:
    team_router = None

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
if team_router:
    api_router.include_router(team_router, tags=["teams"])  