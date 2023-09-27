from sqlalchemy import Column, Integer, Float, String

from .schemas import engine, Base


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(512), nullable=False)
    title = Column(String(512), nullable=False)
    price = Column(Float, nullable=False)
    target = Column(Float, nullable=False)
    image_url = Column(String(128), nullable=False)


def create_all():
    Base.metadata.create_all(bind=engine)
