from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
from app.db import team_col
from app.services.team_service import distributeWinningsAndDisbandTeam

scheduler = BackgroundScheduler()

def check_and_distribute_finished_teams():
    now = datetime.now(timezone.utc)
    finished_teams = team_col.find({"challenge_end_at": {"$lte": now}})

    for team in finished_teams:
        teamUid = team.get("teamUid")
        try:
            print(f"[AutoDistribution] Processing team {teamUid}")
            distributeWinningsAndDisbandTeam(teamUid)
        except Exception as e:
            print(f"[AutoDistribution] Error processing {teamUid}: {e}")

def start_scheduler():
    # 1분마다 실행
    scheduler.add_job(check_and_distribute_finished_teams, "interval", minutes=1)
    scheduler.start()
