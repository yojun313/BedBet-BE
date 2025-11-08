from pydantic import BaseModel, constr
from typing import Optional, Literal, List
from datetime import datetime

class TeamCreateDto(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=20)] = None
    challenge_start_at: datetime
    challenge_end_at: datetime

class TeamDto(BaseModel):
    id: str
    name: Optional[str]
    owner_id: str
    challenge_start_at: datetime
    challenge_end_at: datetime
    created_at: datetime

class TeamMemberDto(BaseModel):
    team_id: str
    userUid: str
    role: Literal["owner", "member"]
    joined_at: datetime

class MembersResponse(BaseModel):
    members: List[TeamMemberDto]
    next_cursor: Optional[str] = None

class JoinResponse(BaseModel):
    member: TeamMemberDto
    members: List[TeamMemberDto]
    
class TeamWithMembersDto(TeamDto):
    members: List[TeamMemberDto]