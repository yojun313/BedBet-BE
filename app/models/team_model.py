from pydantic import BaseModel, constr
from typing import Optional, Literal, List
from datetime import datetime

class TeamCreateDto(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=20)] = None
    challenge_start_at: datetime
    challenge_end_at: datetime
    coin: int

class TeamJoinDto(BaseModel):
    teamUid: str
    coin: int

class TeamExitDto(BaseModel):
    teamUid: str
