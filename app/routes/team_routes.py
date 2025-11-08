from fastapi import APIRouter, Depends, Header, HTTPException, Query
from typing import Optional
from app.libs.jwt import verify_token
from app.models.team_model import (
    TeamCreateDto, TeamDto, TeamMemberDto, MembersResponse, JoinResponse, TeamWithMembersDto
)
from app.services.team_service import (
    create_team, join_team, list_members, join_team_with_members, get_team_with_members
)
router = APIRouter()

@router.post("/team", response_model=TeamDto, status_code=201)
async def create_team_endpoint(payload: TeamCreateDto, userUid: str = Depends(verify_token)):
    return create_team(userUid, payload)


@router.post("/team/{team_id}/join", response_model=JoinResponse)
async def join_team_endpoint(team_id: str, userUid: str = Depends(verify_token)):
    return join_team_with_members(team_id, userUid)

@router.get("/team/{team_id}", response_model=TeamWithMembersDto)
async def get_team_endpoint(team_id: str, userUid: str = Depends(verify_token)):
    return get_team_with_members(team_id)

@router.get("/team/{team_id}/members", response_model=MembersResponse)
async def list_members_endpoint(
    team_id: str,
    limit: int = Query(20, ge=1, le=200),
    cursor: Optional[str] = None,
    userUid: str = Depends(verify_token),
):
    return list_members(team_id, limit, cursor)
