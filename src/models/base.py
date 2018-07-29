from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MetaBase(Base):
    __abstract__ = True
    def __init_subclass__(cls, *args, **kwargs):
        for name in cls.__slots__:
            setattr(cls, name[1:], property(lambda self, name=name: getattr(self, name)))


