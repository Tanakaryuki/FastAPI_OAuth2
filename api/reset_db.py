from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from api.models.user import Base as UserBase
from api.models.task import Base as TaskBase

load_dotenv(verbose=True)
DATABASE_URL = os.getenv("DATABASE_URL")


def reset_database(db_url):
    engine = create_engine(db_url, echo=True)
    UserBase.metadata.drop_all(bind=engine)
    TaskBase.metadata.drop_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)
    TaskBase.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database(DATABASE_URL)
