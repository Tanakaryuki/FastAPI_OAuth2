from sqlalchemy import func, Column, String, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from api.db import Base, generate_uuid


class Task(Base):
    __tablename__ = "Tasks"

    uuid = Column(String(48), primary_key=True, default=generate_uuid, index=True)
    id = Column(String(48), unique=True, nullable=False, index=True)
    administrator_username = Column(
        String(48), ForeignKey("Users.username"), nullable=False, index=True
    )
    title = Column(String(48), nullable=False)
    detail = Column(String(96), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    administrator = relationship("User", back_populates="tasks_administered")
