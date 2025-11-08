from fastapi import APIRouter, Depends
from app.libs.jwt import verify_token
from app.services.user_service import deleteUser, getUserInfo

router = APIRouter()

@router.get('/info')
def get_user_info(userUid: str = Depends(verify_token)):
    return getUserInfo(userUid)

@router.delete('/')
def delete_user(userUid: str = Depends(verify_token)):
    return deleteUser(userUid)