from fastapi import APIRouter, Depends, Header, HTTPException, Query
from typing import Optional
from app.models.team_model import TeamCreateDto, TeamDto, TeamMemberDto, MembersResponse
from app.services.team_service import create_team, join_team, get_team, list_members

router = APIRouter()

async def get_current_user_id(x_user_id: Optional[str] = Header(None, convert_underscores=False)) -> str:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="X-User-Id header required")
    return x_user_id

@router.post("/team", response_model=TeamDto, status_code=201)
async def create_team_endpoint(payload: TeamCreateDto, user_id: str = Depends(get_current_user_id)):
    return create_team(user_id, payload)

@router.post("/team/{team_id}/join", response_model=TeamMemberDto)
async def join_team_endpoint(team_id: str, user_id: str = Depends(get_current_user_id)):
    return join_team(team_id, user_id)

@router.get("/team/{team_id}", response_model=TeamDto)
async def get_team_endpoint(team_id: str, user_id: str = Depends(get_current_user_id)):
    return get_team(team_id)

@router.get("/team/{team_id}/members", response_model=MembersResponse)
async def list_members_endpoint(
    team_id: str,
    limit: int = Query(20, ge=1, le=200),
    cursor: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
):
    return list_members(team_id, limit, cursor)
