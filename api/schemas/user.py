from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserSignupRequest(BaseModel):
    email: EmailStr = Field(..., example="example@example.com")
    password: str = Field(..., example="password")
    username: str = Field(..., example="admin")
    display_name: str = Field(..., example="福岡太郎")
    is_admin: bool = Field(..., example=True)

    class Config:
        from_attributes = True
        
class UserInformationResponse(BaseModel):
    uuid: str
    email: EmailStr
    username: str
    display_name: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
