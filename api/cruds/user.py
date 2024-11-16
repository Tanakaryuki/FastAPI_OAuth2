from sqlalchemy.orm import Session

import api.models.user as user_model

from passlib.context import CryptContext


def create_user(db: Session, user: user_model.User) -> user_model.User | None:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read_user_by_username(db: Session, username: str) -> user_model.User | None:
    return (
        db.query(user_model.User).filter(user_model.User.username == username).first()
    )


def read_user_by_email(db: Session, email: str) -> user_model.User | None:
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def exist_refresh_token_by_username(db: Session, username: str) -> bool:
    db_token = (
        db.query(user_model.RefreshToken)
        .filter(user_model.RefreshToken.user_username == username)
        .first()
    )
    return db_token is not None


def create_refresh_token(
    db: Session, refresh_token: user_model.RefreshToken
) -> user_model.RefreshToken | None:
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token


def update_refresh_token(db: Session, username: str, refresh_token: str):
    db_refresh_token = (
        db.query(user_model.RefreshToken)
        .filter(user_model.RefreshToken.user_username == username)
        .first()
    )
    db_refresh_token.refresh_token = refresh_token
    db.commit()
    db.refresh(db_refresh_token)
    return db_refresh_token


def is_refresh_token_valid(db: Session, refresh_token: str, username: str) -> bool:
    db_token = (
        db.query(user_model.RefreshToken)
        .filter(
            user_model.RefreshToken.refresh_token == refresh_token,
            user_model.RefreshToken.user_username == username,
        )
        .first()
    )
    return db_token is not None
