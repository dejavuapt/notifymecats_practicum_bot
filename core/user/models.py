from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
