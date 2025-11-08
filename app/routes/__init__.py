from .auth_routes import router as auth_router
from .coin_routes import router as coin_router
from .money_routes import router as money_router
from .team_routes import router as team_router
from fastapi import APIRouter, Depends
from app.libs.jwt import verify_token

try:
    from .team_routes import router as team_router 
except Exception:
    team_router = None

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(team_router, tags=["team"], dependencies=[Depends(verify_token)])
api_router.include_router(coin_router, prefix="/coin", tags=["coin"], dependencies=[Depends(verify_token)])
api_router.include_router(money_router, prefix="/money", tags=["money"], dependencies=[Depends(verify_token)])
