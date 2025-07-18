import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    email: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    access_token: str
    refresh_token: str

class DataToken(BaseModel):
    id:Optional[int] = None

class UserOutput(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

class LoginResponse(UserOutput):
    access_token: str
    token_type: str