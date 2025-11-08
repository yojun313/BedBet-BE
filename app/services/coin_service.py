from app.models.coin_model import CoinRequestDto
from fastapi.responses import JSONResponse
from app.db import coin_col, user_col
from app.db import clean_doc

def getCoinPendingRequests():
    pending_requests = list(coin_col.find())
    for request in pending_requests:
        request['_id'] = str(request['_id'])
    return JSONResponse(status_code=200, content={"pending_requests": pending_requests})

def requestCoin(coinRequestDto: CoinRequestDto, userUid: str):
    coinRequestDict = coinRequestDto.model_dump()
    amount = coinRequestDict['amount']
    
    existing_record = coin_col.find_one({"userUid": userUid})
    if existing_record:
        return JSONResponse(status_code=400, content={"message": "Coin request already exists"})
    
    existing_user = user_col.find_one({"userUid": userUid})
    if not existing_user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    existing_user = clean_doc(existing_user)
    
    coin_col.insert_one({
        "name": existing_user['name'],
        "userUid": userUid,
        "amount": amount,
    })
    return JSONResponse(status_code=200, content={"message": "Coin request submitted successfully"})

def cancelRequestCoin(userUid: str):
    result = coin_col.delete_one({"userUid": userUid})
    if result.deleted_count == 0:
        return JSONResponse(status_code=404, content={"message": "No coin request found to cancel"})  
    return JSONResponse(status_code=200, content={"message": "Coin request cancelled successfully"})

def giveCoin(userUid: str):
    user_record = coin_col.find_one({"userUid": userUid})
    if not user_record:
        return JSONResponse(status_code=404, content={"message": "User request not found"})
    
    requested_amount = user_record.get("amount", 0)
    user_col.update_one(
        {"userUid": userUid},
        {"$inc": {"coin": requested_amount}}
    )
    coin_col.delete_one({"userUid": userUid})
    
    return JSONResponse(status_code=200, content={"message": "Coins granted successfully"})

    
    
