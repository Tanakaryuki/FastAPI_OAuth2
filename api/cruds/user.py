from sqlalchemy.orm import Session

import api.models.user as user_model
import api.schemas.user as user_schema

from passlib.context import CryptContext


def creatr_user(db: Session, signup: user_schema.UserSignupRequest) -> user_model.User | None:
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