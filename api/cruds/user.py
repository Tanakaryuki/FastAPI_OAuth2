from sqlalchemy.orm import Session

import api.models.user as user_model
import api.schemas.user as user_schema

from passlib.context import CryptContext


def create_user(db: Session, signup: user_schema.UserSignupRequest) -> user_model.User | None:
    signup_dict = signup.model_dump()
    signup_dict.pop("password", None)
    hashed_password = CryptContext(["bcrypt"]).hash(signup.password)
    user = user_model.User(
        hashed_password=hashed_password, **signup_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def read_user_by_username(db: Session, username: str) -> user_model.User | None:
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def create_refresh_token(db: Session, username: str, refresh_token: str):
    db_refresh_token = db.query(user_model.RefreshToken).filter(user_model.RefreshToken.user_username == username).first()
    if db_refresh_token:
        db_refresh_token.refresh_token = refresh_token
    else:
        db_refresh_token = user_model.RefreshToken(user_username=username, refresh_token=refresh_token)
        db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)
    return db_refresh_token

def read_refresh_token(db: Session, refresh_token: str,username: str) -> bool:
    db_token = db.query(user_model.RefreshToken).filter(user_model.RefreshToken.refresh_token == refresh_token,user_model.RefreshToken.user_username == username).first()
    return db_token is not None
