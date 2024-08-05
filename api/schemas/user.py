from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime


class UserSignupRequest(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "example@example.com"})
    password: str = Field(..., json_schema_extra={"example": "password"})
    username: str = Field(..., json_schema_extra={"example": "admin"})
    display_name: str = Field(..., json_schema_extra={"example": "福岡太郎"})
    is_admin: bool = Field(..., json_schema_extra={"example": "true"})

    model_config = ConfigDict()
        
class UserInformationResponse(BaseModel):
    uuid: str
    email: EmailStr
    username: str
    display_name: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
