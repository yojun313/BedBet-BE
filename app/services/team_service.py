from datetime import datetime, timezone
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.db import team_col, user_col, clean_doc
from app.models.team_model import TeamCreateDto, TeamJoinDto, TeamExitDto
import uuid
from zoneinfo import ZoneInfo
from fastapi.encoders import jsonable_encoder


def _to_kst(dt: datetime) -> datetime:
    """입력 datetime을 KST(Asia/Seoul)로 변환. naive이면 KST로 간주."""
    kst = ZoneInfo("Asia/Seoul")
    if dt.tzinfo is None:
        return dt.replace(tzinfo=kst)
    return dt.astimezone(kst)

def _is_kst_30min_aligned(dt: datetime) -> bool:
    kst_dt = _to_kst(dt)
    return (kst_dt.minute % 30 == 0) and kst_dt.second == 0 and kst_dt.microsecond == 0
    
def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def getTeams():
    teams = team_col.find()
    teams = [clean_doc(team) for team in teams]
    return {"status_code": 200, "message": "Get teams success", "teams": teams}

def createTeam(ownerUid: str, teamCreateDto: TeamCreateDto):
    team = teamCreateDto.model_dump()
    
    existing_room = team_col.find_one({"ownerUid": ownerUid})
    if existing_room:
        raise HTTPException(status_code=409, detail={"message": "This user already owns a team."})
    
    existing_name = team_col.find_one({"name": team.get("name")})
    if existing_name:
        raise HTTPException(status_code=409, detail={"message": "Team name already exists."})
    
    start_at = team.get("challenge_start_at")
    end_at = team.get("challenge_end_at")
    if not (isinstance(start_at, datetime) and isinstance(end_at, datetime)):
        raise HTTPException(status_code=400, detail={"message": "challenge_start_at and challenge_end_at must be datetime."})

    if not _is_kst_30min_aligned(start_at) or not _is_kst_30min_aligned(end_at):
        raise HTTPException(status_code=400, detail={"message": "Start and end must be aligned to 30-minute boundaries in KST."})

    if _to_kst(start_at) >= _to_kst(end_at):
        raise HTTPException(status_code=400, detail={"message": "challenge_start_at must be before challenge_end_at."})
    
    user = user_col.find_one({"userUid": ownerUid})
    if not user:
        raise HTTPException(status_code=404, detail={"message": "User not found."})
    
    if team.get("coin") > user.get("coin", 0):
        raise HTTPException(status_code=400, detail={"message": "Insufficient coins to create the team."})
    
    teamUid = str(uuid.uuid4())
    team_col.insert_one({
        "name": team.get("name"),
        "teamUid": teamUid,
        "ownerUid": ownerUid,
        "challenge_start_at": start_at,
        "challenge_end_at": end_at,
        "created_at": now_utc(),
        "teammates": [{"userUid": ownerUid, "coin": team.get("coin")}],
        "bet_coins": team.get("coin"),
    })
    
    user_col.update_one(
        {"userUid": ownerUid},
        {"$set": {"teamUid": teamUid}}
    )
    return JSONResponse(status_code=201, content={"message": "Team created successfully", "teamUid": teamUid})
    
def joinTeam(teamJoinDto: TeamJoinDto, userUid: str):
    teamJoinDict = teamJoinDto.model_dump()
    
    teamUid = teamJoinDict["teamUid"]
    coin = teamJoinDict["coin"]
    
    team = team_col.find_one({"teamUid": teamUid})
    if not team:
        raise HTTPException(status_code=404, detail={"message": "Team not found."})

    if any(member.get("userUid") == userUid for member in team.get("teammates", [])):
         raise HTTPException(status_code=409, detail={"message": "User already a member of the team."})
    
    user = user_col.find_one({"userUid": userUid})
    if not user:
        raise HTTPException(status_code=404, detail={"message": "User not found."})
    
    if user.get("teamUid"):
        raise HTTPException(status_code=400, detail={"message": "User already belongs to a team."})
    
    if coin > user.get("coin", 0):
        raise HTTPException(status_code=400, detail={"message": "Insufficient coins to join the team."})
    
    # 팀 멤버로 추가 & 팀 베팅 코인 증가
    team_col.update_one(
        {"teamUid": teamUid},
        {"$addToSet": {"teammates": {"userUid": userUid, "coin": coin}}, "$inc": {"bet_coins": coin}}
    )
    
    # 유저 코인 감소 & 팀 정보 업데이트
    user_col.update_one(
        {"userUid": userUid},
        {"$inc": {"coin": -coin}, "$set": {"teamUid": teamUid}}
    )
    
    return JSONResponse(status_code=200, content={"message": "Successfully joined team"})
    
def getTeamInfo(teamUid: str):
    team = team_col.find_one({"teamUid": teamUid})
    team = clean_doc(team)
    if not team:
        raise HTTPException(status_code=404, detail={"message": "Team not found."})

    team = clean_doc(team) or {}
    # datetime/ObjectId 등 안전하게 직렬화
    team_serializable = jsonable_encoder(team)
    return JSONResponse(status_code=200, content={"message": "Get team info success", "team": team_serializable})

def exitTeam(teamExitDto: TeamExitDto, userUid: str):
    teamUid = teamExitDto.model_dump().get("teamUid")
    team = team_col.find_one({"teamUid": teamUid})
    if not team:
        raise HTTPException(status_code=404, detail={"message": "Team not found."})
    
    if not any(member.get("userUid") == userUid for member in team.get("teammates", [])):
        raise HTTPException(status_code=400, detail={"message": "User is not a member of the team."})
    
    challenge_start_at = team.get("challenge_start_at")
    if not isinstance(challenge_start_at, datetime):
        raise HTTPException(status_code=500, detail={"message": "Invalid challenge_start_at in DB."})
    
    challenge_start_at_utc = _to_kst(challenge_start_at).astimezone(timezone.utc)
    if now_utc() >= challenge_start_at_utc:
        raise HTTPException(status_code=400, detail={"message": "Cannot exit team after challenge has started."})
    
    member = next((m for m in team.get("teammates", []) if m.get("userUid") == userUid), None)
    refund_coins = member.get("coin", 0) if member else 0
    
    # 팀 멤버에서 제거
    team_col.update_one(
        {"teamUid": teamUid},
        {
            "$pull": {"teammates": {"userUid": userUid}},
            "$inc": {"bet_coins": -refund_coins}
        }
    )
    
    # 유저의 팀 정보 초기화 & 코인 환불
    user_col.update_one(
        {"userUid": userUid},
        {"$inc": {"coin": refund_coins}, "$set": {"teamUid": ""}}
    )
    return JSONResponse(status_code=200, content={"message": "Successfully exited the team."})
    