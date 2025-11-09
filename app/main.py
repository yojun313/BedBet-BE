from fastapi import FastAPI, Request
from app.routes import api_router
from app.db import team_col
from app.services.team_service import distributeWinningsAndDisbandTeam  # 기존 함수 import
import gc
import asyncio
from datetime import datetime, timezone
from rich.console import Console
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

console = Console()

# 주기적으로 GC 실행
async def periodic_gc(interval_seconds: int = 60):
    while True:
        await asyncio.sleep(interval_seconds)
        gc.collect()

async def periodic_team_cleanup(interval_seconds: int = 60):
    """challenge_end_at이 지난 팀 자동 정산 및 삭제"""
    while True:
        await asyncio.sleep(interval_seconds)
        now = datetime.now(timezone.utc)
        expired_teams = list(team_col.find({"challenge_end_at": {"$lte": now}}))

        if not expired_teams:
            continue

        console.print(f"[bold yellow]{len(expired_teams)}[/bold yellow] team(s) found for auto distribution.")
        for team in expired_teams:
            teamUid = team.get("teamUid")
            try:
                console.print(f"[cyan]→ Processing team {teamUid}[/cyan]")
                distributeWinningsAndDisbandTeam(teamUid)
                console.print(f"[green]✔ Team {teamUid} distributed and deleted.[/green]")
            except Exception as e:
                console.print(f"[red]✖ Error processing team {teamUid}: {e}[/red]")


# 요청 로그 미들웨어 (텍스트 출력)
class RichLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now()
        response = await call_next(request)
        duration = (datetime.now() - start_time).total_seconds()

        method = request.method
        path = request.url.path
        status = response.status_code
        duration_str = f"{duration:.2f}s"
        time_str = start_time.strftime("%H:%M:%S")

        status_str = str(status)
        if 200 <= status < 300:
            status_str = f"[green]{status}[/green]"
        elif 300 <= status < 400:
            status_str = f"[yellow]{status}[/yellow]"
        else:
            status_str = f"[red]{status}[/red]"

        log_message = (
            f"[dim]{time_str}[/dim] "
            f"{status_str} "
            f"[cyan]{method}[/cyan] "
            f"[green]{path}[/green] "
            f"[yellow]{duration_str}[/yellow]"
        )

        console.print(log_message)
        return response

# FastAPI 앱 구성
app = FastAPI()
app.add_middleware(RichLoggerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*", 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(periodic_gc(60))
    asyncio.create_task(periodic_team_cleanup(60))

@app.on_event("shutdown")
async def stop_background_tasks():
    pass  # 따로 종료할 작업 없음

app.include_router(api_router, prefix="/api", tags=["API"])
