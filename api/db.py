from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
DATABASE_URL = str(os.getenv("DATABASE_URL"))

engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(engine)

Base = declarative_base()


def get_db():
    database = LocalSession()
    try:
        yield database
    finally:
        database.close()


def generate_uuid():
    return str(uuid4())