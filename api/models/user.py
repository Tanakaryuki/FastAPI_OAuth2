from sqlalchemy import func, Column,String, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from api.db import Base, generate_uuid


class User(Base):
    __tablename__ = "Users"

    uuid = Column(String(48), default=generate_uuid,
                  primary_key=True, index=True)
    id = Column(String(48), unique=True, nullable=False, index=True)
    email = Column(String(48), unique=True, nullable=False)
    hashed_password = Column(String(96), nullable=False)
    display_name = Column(String(96), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    tasks_administered = relationship("Task", back_populates="administrator")