from datetime import datetime, timezone
from typing import Optional, List
from bson import ObjectId
from fastapi import HTTPException
from app.db import team_col, team_members_col
from app.models.team_model import (
    TeamCreateDto, TeamDto, TeamMemberDto, MembersResponse, TeamWithMembersDto, JoinResponse
)
from pymongo import ReturnDocument


def _to_oid(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail={"code": "BAD_TEAM_ID", "message": "team_id 형식이 올바르지 않습니다."})

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def create_team(owner_id: str, team: TeamCreateDto) -> TeamDto:
    doc = {
        "name": team.name,
        "owner_id": owner_id,
        "challenge_start_at": team.challenge_start_at,
        "challenge_end_at": team.challenge_end_at,
        "created_at": now_utc(),
    }
    try:
        res = team_col.insert_one(doc)
    except Exception as e:
        if "E11000" in str(e):
            raise HTTPException(status_code=409, detail={"code":"TEAM_NAME_CONFLICT","message":"같은 이름의 팀이 이미 존재합니다!"})
        raise
    team_id = res.inserted_id
  
    team_members_col.update_one(
        {"team_id": team_id, "userUid": owner_id},
        {"$setOnInsert": {"role": "owner", "joined_at": now_utc()}},
        upsert=True,
    )
    return TeamDto(
        id=str(team_id),
        name=doc.get("name"),
        owner_id=owner_id,
        challenge_start_at=doc["challenge_start_at"],
        challenge_end_at=doc["challenge_end_at"],
        created_at=doc["created_at"],
    )

def join_team(team_id: str, userUid: str) -> TeamMemberDto:
    tid = _to_oid(team_id)  
    team = team_col.find_one({"_id": tid})
    if not team:
        raise HTTPException(status_code=404, detail={"code":"TEAM_NOT_FOUND","message":"팀이 존재하지 않습니다."})


    doc = team_members_col.find_one_and_update(
        {"team_id": tid, "userUid": userUid},
        {"$setOnInsert": {"role": "member", "joined_at": now_utc()}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

    return TeamMemberDto(
        team_id=str(doc["team_id"]),
        userUid=doc["userUid"],
        role=doc["role"],
        joined_at=doc["joined_at"],
    )

def get_team(team_id: str) -> TeamDto:
    tid = _to_oid(team_id)  
    team = team_col.find_one({"_id": tid})
    if not team:
        raise HTTPException(status_code=404, detail={"code":"TEAM_NOT_FOUND","message":"팀이 존재하지 않습니다."})
    return TeamDto(
        id=str(team["_id"]),
        name=team.get("name"),
        owner_id=team["owner_id"],
        challenge_start_at=team.get("challenge_start_at"),
        challenge_end_at=team.get("challenge_end_at"),
        created_at=team["created_at"],
    )

def list_members(team_id: str, limit: int = 20, cursor: Optional[str] = None) -> MembersResponse:
    tid = _to_oid(team_id)
    query = {"team_id": tid}
    if cursor:
        query["_id"] = {"$gt": ObjectId(cursor)}
    docs: List[dict] = list(team_members_col.find(query).sort("_id", 1).limit(limit))
    members = [
        TeamMemberDto(team_id=str(d["team_id"]), userUid=d["userUid"], role=d["role"], joined_at=d["joined_at"])
        for d in docs
    ]
    next_cursor = str(docs[-1]["_id"]) if len(docs) == limit else None
    return MembersResponse(members=members, next_cursor=next_cursor)

def join_team_with_members(team_id: str, userUid: str) -> JoinResponse:

    member = join_team(team_id, userUid)

    members_resp = list_members(team_id, limit=200)
    return JoinResponse(member=member, members=members_resp.members)

def get_team_with_members(team_id: str) -> TeamWithMembersDto:
    tid = _to_oid(team_id)
    team = team_col.find_one({"_id": tid})
    if not team:
        raise HTTPException(status_code=404, detail={"code":"TEAM_NOT_FOUND","message":"팀이 존재하지 않습니다."})
    docs: List[dict] = list(team_members_col.find({"team_id": tid}).sort("_id", 1))
    members = [
        TeamMemberDto(
            team_id=str(d["team_id"]),
            userUid=d["userUid"],
            role=d["role"],
            joined_at=d["joined_at"],
        )
        for d in docs
    ]

    return TeamWithMembersDto(
        id=str(team["_id"]),
        name=team.get("name"),
        owner_id=team["owner_id"],
        challenge_start_at=team.get("challenge_start_at"),
        challenge_end_at=team.get("challenge_end_at"),
        created_at=team["created_at"],
        members=members,
    )