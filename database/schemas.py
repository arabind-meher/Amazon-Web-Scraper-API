import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv(os.path.join('credentials.env'))

USERNAME = os.environ.get('_USERNAME')
PASSWORD = os.environ.get('_PASSWORD')

HOST = os.environ.get('_HOST')
PORT = os.environ.get('_PORT')

DATABASE = os.environ.get('_DATABASE')

SQLALCHEMY_DATABASE_URI = f'mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
