from app.models.auth_model import VerifyRequestDto
from app.db import auth_col
from app.utils.mail import sendEmail
import random
from fastapi.responses import JSONResponse


def verifyRequest(verifyEmailDto: VerifyRequestDto):
    verifyRequestDict = verifyEmailDto.model_dump()
    email = verifyRequestDict['email']
    code = ''.join(random.choices('0123456789', k=6))
    
    auth_col.update_one(
        {"email": email},
        {"$set": {"code": code}},
        upsert=True
    )
    
    msg = (
        f"인증 번호 '{code}'를 입력하십시오"
    )
    sendEmail(email, "[BedBet] 회원가입 인증번호", msg)
    
    return JSONResponse(status_code=200, content={"message": "Verification code sent"})
