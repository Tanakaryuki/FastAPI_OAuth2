from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserSignupRequest(BaseModel):
    email: EmailStr = Field(..., example="example@example.com")
    password: str = Field(..., example="password")
    id: str = Field(..., example="admin")
    display_name: str = Field(..., example="福岡太郎")
    is_admin: bool = Field(..., example=True)

    class Config:
        from_attributes = True