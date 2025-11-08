from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException
from bson import ObjectId
from app.db import team_col, team_members_col
from app.models.team_model import TeamCreateDto, TeamDto, TeamMemberDto, MembersResponse

def now_utc():
    return datetime.now(timezone.utc)

def create_team(owner_id: str, team: TeamCreateDto) -> TeamDto:
    doc = {
        "name": team.name,
        "owner_id": owner_id,
        "created_at": now_utc()
    }
    try:
        result = team_col.insert_one(doc)
    except Exception as e:
        if "E11000" in str(e):
            raise HTTPException(status_code=409, detail={"code": "TEAM_NAME_CONFLICT", "message": "같은 이름의 팀이 이미 존재합니다!"})
        raise
    team_id = result.inserted_id

    team_members_col.update_one(
        {"team_id": team_id, "userUid": owner_id},
        {"$setOnInsert": {"role": "owner", "joined_at": now_utc()}},
        upsert=True
    )
    doc["_id"] = team_id
    return TeamDto(id=str(team_id), name=doc.get("name"), owner_id=owner_id, created_at=doc["created_at"])

def join_team(team_id: str, userUid: str) -> TeamMemberDto:
    tid = ObjectId(team_id)
    team = team_col.find_one({"_id": tid})
    if not team:
        raise HTTPException(status_code=404, detail={"code": "TEAM_NOT_FOUND", "message": "팀이 존재하지 않습니다."})
    existing = team_members_col.find_one({"team_id": tid, "userUid": userUid})
    if existing:
        return TeamMemberDto(team_id=team_id, userUid=userUid, role=existing["role"], joined_at=existing["joined_at"])
    doc = {"team_id": tid, "userUid": userUid, "role": "member", "joined_at": now_utc()}
    try:
        team_members_col.insert_one(doc)
    except Exception as e:
        if "E11000" in str(e):
            existing = team_members_col.find_one({"team_id": tid, "userUid": userUid})
            return TeamMemberDto(team_id=team_id, userUid=userUid, role=existing["role"], joined_at=existing["joined_at"])
        raise
    return TeamMemberDto(**doc, team_id=team_id, userUid=userUid)

def get_team(team_id: str) -> TeamDto:
    tid = ObjectId(team_id)
    team = team_col.find_one({"_id": tid})
    if not team:
        raise HTTPException(status_code=404, detail={"code": "TEAM_NOT_FOUND", "message": "팀이 존재하지 않습니다."})
    return TeamDto(id=str(team["_id"]), name=team.get("name"), owner_id=team["owner_id"], created_at=team["created_at"])

def list_members(team_id: str, limit: int = 20, cursor: Optional[str] = None) -> MembersResponse:
    tid = ObjectId(team_id)
    query = {"team_id": tid}
    if cursor:
        query["_id"] = {"$gt": ObjectId(cursor)}
    docs = team_members_col.find(query).sort("_id", 1).limit(limit)
    members = [TeamMemberDto(team_id=str(d["team_id"]), userUid=d["userUid"], role=d["role"], joined_at=d["joined_at"]) for d in docs]
    next_cursor = None
    if len(members) == limit:
        next_cursor = str(members[-1].joined_at) 
    return MembersResponse(members=members, next_cursor=next_cursor)
