from fastapi import APIRouter, Depends
from app.libs.jwt import verify_token
from app.models.team_model import TeamCreateDto, TeamJoinDto, TeamExitDto
from app.services.team_service import createTeam, joinTeam, exitTeam, getTeamInfo, getTeams

router = APIRouter()

@router.get("/teams")
async def get_teams():
    return getTeams()

@router.post("/team/create")
async def creaet_team(teamCreateDto: TeamCreateDto, userUid: str = Depends(verify_token)):
    return createTeam(userUid, teamCreateDto)

@router.post("/team/join")
async def join_team(teamJoinDto: TeamJoinDto, userUid: str = Depends(verify_token)):
    return joinTeam(teamJoinDto, userUid)

@router.post("/team/exit")
async def exit_team(teamExitDto: TeamExitDto, userUid: str = Depends(verify_token)):
    return exitTeam(teamExitDto, userUid)

@router.get("/team/info/{teamUid}")
async def get_team_info(teamUid: str):
    return getTeamInfo(teamUid)

