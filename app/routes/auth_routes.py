from fastapi import APIRouter, Query, Header
from app.models.auth_model import VerifyRequestDto, VerifyEmailDto, SignUpDto, SignInDto
from app.services.auth_service import verifyRequest, verifyCode, signUp, signIn

router = APIRouter()

@router.post('/verify/request')
def verify_request(verifyRequestDto: VerifyRequestDto):
    return verifyRequest(verifyRequestDto)

@router.post('/verify/email')
def verify_code(verifyEmailDto: VerifyEmailDto):
    return verifyCode(verifyEmailDto)

@router.post('/signup')
def sign_up(signUpDto: SignUpDto):
    return signUp(signUpDto)

@router.post('/signin')
def sign_in(signInDto: SignInDto):
    return signIn(signInDto)
