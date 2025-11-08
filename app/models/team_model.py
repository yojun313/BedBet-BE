from pydantic import BaseModel, constr
from typing import Optional, Literal, List
from datetime import datetime

class TeamCreateDto(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=20)] = None

class TeamDto(BaseModel):
    id: str
    name: Optional[str]
    owner_id: str
    created_at: datetime

class TeamMemberDto(BaseModel):
    team_id: str
    userUid: str
    role: Literal["owner", "member"]
    joined_at: datetime

class MembersResponse(BaseModel):
    members: List[TeamMemberDto]
    next_cursor: Optional[str] = None
