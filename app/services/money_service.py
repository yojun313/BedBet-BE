from app.models.money_model import MoneyRequestDto
from fastapi.responses import JSONResponse
from app.db import money_col, user_col
from app.db import clean_doc

def getMoneyPendingRequests():
    pending_requests = list(money_col.find())
    for request in pending_requests:
        request['_id'] = str(request['_id'])
    return JSONResponse(status_code=200, content={"pending_requests": pending_requests})

def requestMoney(moneyRequestDto: MoneyRequestDto, userUid: str):
    coinRequestDict = moneyRequestDto.model_dump()
    amount = coinRequestDict['amount']
    
    existing_record = money_col.find_one({"userUid": userUid})
    if existing_record:
        return JSONResponse(status_code=400, content={"message": "Money request already exists"})
    
    
    user = user_col.find_one({"userUid": userUid})
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    
    user = clean_doc(user)
    user_coin = user.get("coin", 0)
    required_coins = int(amount / 110)
    
    if required_coins > user_coin:
        return JSONResponse(status_code=400, content={"message": "Not enough coins to request money"})
    
    money_col.insert_one({
        "name": user['name'],
        "userUid": userUid,
        "amount": amount,
    })
    return JSONResponse(status_code=200, content={"message": "Money request submitted successfully"})

def cancelRequestMoney(userUid: str):
    result = money_col.delete_one({"userUid": userUid})
    if result.deleted_count == 0:
        return JSONResponse(status_code=404, content={"message": "No money request found to cancel"})  
    return JSONResponse(status_code=200, content={"message": "Money request cancelled successfully"})

def giveMoney(userUid: str):
    user_record = money_col.find_one({"userUid": userUid})
    if not user_record:
        return JSONResponse(status_code=404, content={"message": "Money request not found"})
    
    requested_amount = user_record.get("amount", 0)
    coin = int(requested_amount / 110)
    
    user_col.update_one(
        {"userUid": userUid},
        {"$inc": {"coin": -coin}}
    )
    money_col.delete_one({"userUid": userUid})
    
    return JSONResponse(status_code=200, content={"message": "Money granted successfully"})

    
    
