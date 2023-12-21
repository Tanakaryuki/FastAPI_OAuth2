from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

import api.schemas.user as user_schema
import api.cruds.user as user_crud
import api.models.user as user_model
from api.db import get_db


router = APIRouter()


@router.post("/signup", description="新しいアカウントを作成するために使用されます。", tags=["users"])
def signup(request: user_schema.UserSignupRequest, db: Session = Depends(get_db)):
    user = user_crud.read_user_by_username(db, id=request.id)
    if user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = user_crud.creatr_user(db, request)
    return status.HTTP_201_CREATED
