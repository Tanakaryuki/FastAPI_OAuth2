from sqlalchemy.orm import Session
from datetime import datetime, timezone
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

import api.cruds.user as user_crud
import api.models.user as user_model
import api.schemas.user as user_schema
import api.utils.auth as auth

load_dotenv(verbose=True)
SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))


def signup(
    db: Session, signup: user_schema.UserSignupRequest
) -> user_model.User | ValueError:
    if user_crud.read_user_by_username(db, username=signup.username):
        raise ValueError("User already exists")
    if user_crud.read_user_by_email(db, email=signup.email):
        raise ValueError("Email already exists")
    hashed_password = CryptContext(["bcrypt"]).hash(signup.password)
    user: user_model.User = user_model.User(
        username=signup.username,
        email=signup.email,
        hashed_password=hashed_password,
        display_name=signup.display_name,
        is_admin=signup.is_admin,
    )
    return user_crud.create_user(db, user=user)


def login(db: Session, username: str, password: str) -> user_schema.Token | ValueError:
    user = auth.authenticate_user(db=db, username=username, password=password)
    if not user:
        raise ValueError("Invalid credentials")
    access_token = auth.create_access_token(data={"sub": user.username})
    refresh_token = auth.create_refresh_token(data={"sub": user.username})
    if user_crud.exist_refresh_token_by_username(db=db, username=user.username):
        user_crud.update_refresh_token(
            db=db, username=user.username, refresh_token=refresh_token
        )
    else:
        refresh_token_obj = user_model.RefreshToken(
            user_username=user.username, refresh_token=refresh_token
        )
        user_crud.create_refresh_token(db=db, refresh_token=refresh_token_obj)
    return user_schema.Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


def refresh_access_token(
    db: Session, refresh_token: str
) -> user_schema.Token | ValueError:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise ValueError("Decoding failed")
    username: str | None = payload.get("sub")
    exp: str | None = payload.get("exp")
    if username is None or exp is None:
        raise ValueError("Decoding failed")
    if not user_crud.is_refresh_token_valid(
        db=db, refresh_token=refresh_token, username=username
    ):
        raise ValueError("Refresh token does not exist")
    if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, timezone.utc):
        raise ValueError("Refresh token has expired")
    access_token = auth.create_access_token(data={"sub": username})
    return user_schema.Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
