from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.sqltypes import Date
from config import USER
import settings
import datetime

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_jobs_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Jobs(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = USER

    id = Column(Integer, primary_key=True)
    url = Column('url', String, nullable=True, unique=True)
    name = Column('name', String, nullable=True)
    email = Column('email', String, nullable=True, unique=True)
    phone = Column('phone', String,  nullable=True)
    date = Column('date', Date, nullable=True, default=datetime.datetime.now())
    processed = Column('processed', Boolean, default=False)