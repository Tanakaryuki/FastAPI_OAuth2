from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone
from jose import jwt, JWTError
import os

import api.schemas.user as user_schema
import api.cruds.user as user_crud
import api.models.user as user_model
from api.db import get_db
from api.utils.auth import authenticate_user, create_access_token, create_refresh_token, get_current_user

router = APIRouter()

load_dotenv(verbose=True)
SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))

@router.post("/signup", description="新しいアカウントを作成するために使用されます。")
def signup(request: user_schema.UserSignupRequest, db: Session = Depends(get_db)):
    user = user_crud.read_user_by_username(db, username=request.username)
    if user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = user_crud.create_user(db, request)
    return status.HTTP_201_CREATED

@router.get("/user/me", description="ログインしているユーザの情報を取得するために使用されます", response_model=user_schema.UserInformationResponse)
def get_current_user_info(current_user: user_model.User = Depends(get_current_user)):
    return current_user

@router.post("/token", description="アクセストークンを取得するために使用されます。", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    user_crud.create_refresh_token(db=db, user_uuid=user.uuid, refresh_token=refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/token/refresh", description="リフレッシュトークンから新しいアクセストークンを取得するために使用されます。", response_model=user_schema.Token)
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp: str = payload.get("exp")
        print(username, exp)
        if username is None or exp is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="decode失敗")
        print(user_crud.read_refresh_token(db=db, refresh_token=refresh_token))
        if not user_crud.read_refresh_token(db=db, refresh_token=refresh_token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token が存在しない")
        if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(data={"sub": username})
    return {"refresh_token":refresh_token,"access_token": access_token, "token_type": "bearer"}
