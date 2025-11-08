from fastapi import APIRouter, Query, Header
from app.models.auth_model import VerifyRequestDto
from app.services.auth_service import verifyRequest

router = APIRouter()

@router.post('/verify/request')
def verify_request(verifyRequestDto: VerifyRequestDto):
    return verifyRequest(verifyRequestDto)
