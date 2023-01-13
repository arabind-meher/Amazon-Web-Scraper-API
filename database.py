from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:meher@localhost/amazon'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def connect_db():
    try:
        db = session()
        yield db
    finally:
        db.close()
