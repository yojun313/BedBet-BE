from pydantic import BaseModel

class VerifyRequestDto(BaseModel):
    email: str

class VerifyEmailDto(BaseModel):
    email: str
    code: str

class AuthModel(BaseModel):
    email: str
    code: str

