from sqlalchemy import create_engine
from api.models.user import Base
from api.models.task import Base
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
DATABASE_URL = str(os.getenv("DATABASE_URL"))


def reset_database(db_url):
    engine = create_engine(db_url, echo=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database(DATABASE_URL)