from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from datetime import datetime,timedelta
from dotenv import load_dotenv

import api.schemas.user as user_schema
import api.cruds.user as user_crud
import api.models.user as user_model
from api.db import get_db

load_dotenv()
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

def _get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = user_crud.read_user_by_username(db=db,username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

def _authenticate_user(db: Session, username: str,password: str)-> user_model.User | None:
    user = user_crud.read_user_by_username(db=db,username=username)
    if user is None:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def _create_access_token(data: dict, expires_delta: timedelta|None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup", description="新しいアカウントを作成するために使用されます。", tags=["users"])
def signup(request: user_schema.UserSignupRequest, db: Session = Depends(get_db)):
    user = user_crud.read_user_by_username(db, username=request.username)
    if user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = user_crud.creatr_user(db, request)
    return status.HTTP_201_CREATED

@router.get("/user/me", description="ログインしているユーザの情報を取得するために使用されます", tags=["users"], response_model=user_schema.UserInformationResponse)
def signin(current_user: user_model.User = Depends(_get_current_user)):
    return current_user

@router.post("/token", description="アクセストークンを取得するために使用されます。", tags=["users"], response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = _authenticate_user(db=db,username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}