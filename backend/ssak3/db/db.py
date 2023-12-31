from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv("db_user_name")
user_password = os.getenv("db_user_password")
db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_name = os.getenv("db_name")


DATABASE_URL = f'mysql+pymysql://{user_name}:{user_password}@{db_host}:{db_port}/{db_name}?charset=utf8'

ENGINE = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=ENGINE)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()