from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import api.schemas.user as user_schema
import api.models.user as user_model
import api.services.user as user_service
import api.utils.auth as auth
from api.db import get_db

router = APIRouter()


@router.post("/signup", description="新しいアカウントを作成するために使用されます。")
def signup(request: user_schema.UserSignupRequest, db: Session = Depends(get_db)):
    try:
        user_service.signup(db=db, signup=request)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": "User created"}
    )


@router.get(
    "/user/me",
    description="ログインしているユーザの情報を取得するために使用されます",
    response_model=user_schema.UserInformationResponse,
)
def get_current_user(current_user: user_model.User = Depends(auth.get_current_user)):
    return user_schema.UserInformationResponse(**current_user.__dict__)


@router.post(
    "/token",
    description="アクセストークンを取得するために使用されます。",
    response_model=user_schema.Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    try:
        tokens = user_service.login(
            db=db, username=form_data.username, password=form_data.password
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return tokens


@router.post(
    "/token/refresh",
    description="リフレッシュトークンから新しいアクセストークンを取得するために使用されます。",
    response_model=user_schema.Token,
)
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        tokens = user_service.refresh_access_token(db=db, refresh_token=refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return tokens
