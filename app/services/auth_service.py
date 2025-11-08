from app.models.auth_model import VerifyRequestDto, VerifyEmailDto, SignUpDto, SignInDto, SignInTokenDto
from app.db import auth_col, user_col, clean_doc
from app.utils.mail import sendEmail
import random
from fastapi.responses import JSONResponse
import bcrypt
import jwt
import os
import uuid

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

def verifyCode(verifyEmailDto: VerifyEmailDto):
    verifyCodeDict = verifyEmailDto.model_dump()
    
    email = verifyCodeDict['email']
    code = verifyCodeDict['code']
    record = auth_col.find_one({"email": email})
    
    if not record:
        return JSONResponse(status_code=404, content={"message": "Email not found"})
    if record['code'] != code:
        return JSONResponse(status_code=400, content={"message": "Invalid verification code"})
    
    user_col.update_one(
        {"email": email},
        {
            "$set": {
                "userUid": str(uuid.uuid4()),
                "name": "",
                "email": email,
                "password": "",
                "account_number": "",
                "bank": "",
                "coin": 0,
                "teamUid": "",
            }
        },
        upsert=True
    )
    
    return JSONResponse(status_code=200, content={"message": "Email verified successfully"})

def signUp(signUpDto: SignUpDto):
    signUpDict = signUpDto.model_dump()
    
    email = signUpDict['email']
    
    existing_user = user_col.find_one({"email": email})
    if not existing_user:
        return JSONResponse(status_code=404, content={"message": "Email not verified"})
    
    existing_user = clean_doc(existing_user)
    userUid = existing_user.get('userUid')
    
    name = signUpDict['name']
    password = signUpDict['password']
    account_number = signUpDict['account_number']
    bank = signUpDict['bank']
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_col.update_one(
        {"email": email},
        {
            "$set": {
                "userUid": userUid,
                "name": name,
                "email": email,
                "password": hashed_password,
                "account_number": account_number,
                "bank": bank,
                "coin": 0,
                "teamUid": "",
            }
        }
    )
    
    access_token = create_access_token({"email": email, 'userUid': userUid})
    return JSONResponse(status_code=200, content={"message": "User signed up successfully", "access_token": access_token})

def signIn(signInDto: SignInDto):
    signInDict = signInDto.model_dump()
    email = signInDict['email']
    password = signInDict['password']
    
    user = user_col.find_one({"email": email})
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    user = clean_doc(user)
    stored_hashed_password = user.get('password')
    
    del user['password']
    
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        return JSONResponse(status_code=400, content={"message": "Incorrect password"})
    
    access_token = create_access_token({"email": email, 'userUid': user.get('userUid')})
    return JSONResponse(status_code=200, content={"message": "User signed in successfully", "access_token": access_token, "user": user})
    
def signInToken(signInTokenDto: SignInTokenDto):
    signInTokenDict = signInTokenDto.model_dump()
    payload = jwt.decode(signInTokenDict.get('token'), os.getenv("JWT_SECRET"), algorithms=[os.getenv("JWT_ALGORITHM")])
    user = user_col.find_one({"email": payload.get("email")})
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    user = clean_doc(user)
    del user['password']
    return JSONResponse(status_code=200, content={"message": "Token is valid", "user": user})
    
def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, os.getenv("JWT_SECRET"), algorithm=os.getenv("JWT_ALGORITHM"))
    return encoded_jwt