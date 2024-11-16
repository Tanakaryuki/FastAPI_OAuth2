from sqlalchemy import func, Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base, generate_uuid


class User(Base):
    __tablename__ = "Users"

    uuid = Column(String(48), default=generate_uuid, primary_key=True, index=True)
    username = Column(String(48), unique=True, nullable=False, index=True)
    email = Column(String(48), unique=True, nullable=False)
    hashed_password = Column(String(96), nullable=False)
    display_name = Column(String(96), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    tasks_administered = relationship("Task", back_populates="administrator")
    refresh_tokens = relationship("RefreshToken", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    refresh_token = Column(String(300), nullable=False)
    user_username = Column(
        String(48),
        ForeignKey("Users.username"),
        unique=True,
        index=True,
        nullable=False,
    )
    user = relationship("User", back_populates="refresh_tokens")
