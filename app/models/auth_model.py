from pydantic import BaseModel

class VerifyRequestDto(BaseModel):
    email: str

class VerifyEmailDto(BaseModel):
    email: str
    code: str

class SignUpDto(BaseModel):
    email: str
    name: str
    password: str
    account_number: str
    bank: str

class AuthModel(BaseModel):
    email: str
    code: str

