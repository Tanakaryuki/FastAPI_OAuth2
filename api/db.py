from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+pymysql://root:root_password@aouth_db:3306/demo?charset=utf8"

engine = create_engine(DB_URL)
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