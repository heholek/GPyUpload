from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from ..models.base import Base, MetaBase

def create_db(path, models):
    eng = create_engine('sqlite:///' + path)
    Base.metadata.bind = eng
    Base.metadata.create_all()
    Session = sessionmaker(bind=eng)
    ses = Session
    return ses


def connect_db(path):
    eng = create_engine('sqlite:///' + path)
    Base.metadata.bind = eng
    Session = sessionmaker(bind=eng)
    ses = Session
    return ses

