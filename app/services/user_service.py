from app.db import user_col, team_col, money_col, coin_col
from fastapi.responses import JSONResponse

def getUserInfo(userUid: str):
    user = user_col.find_one({"userUid": userUid})
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    del user['password']
    return JSONResponse(status_code=200, content={"user": user})

def deleteUser(userUid: str):
    user_col.delete_one({"userUid": userUid})
    team_col.update_many(
        {"teammates.userUid": userUid},
        {"$pull": {"teammates": {"userUid": userUid}}}
    )
    money_col.delete_one({"userUid": userUid})
    coin_col.delete_one({"userUid": userUid})   
    
    return JSONResponse(status_code=200, content={"message": "User deleted successfully"})