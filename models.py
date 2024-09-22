from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, declarative_mixin, declared_attr

class Config:
    ENGINE = create_engine('sqlite:///my_db.db')
    BASE = declarative_base()
    SESSION = sessionmaker(bind=ENGINE)

    @classmethod
    def up(cls):
        cls.BASE.metadata.create_all(cls.ENGINE)

    @classmethod
    def down(cls):
        cls.BASE.metadata.drop_all(cls.ENGINE)

@declarative_mixin
class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

class User(Config.BASE):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    phone_number = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

class House(Config.BASE):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    city = Column(String)
    house_type = Column(String)
    pet_friendly = Column(Boolean)

class Job(Config.BASE):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    description = Column(String)
    city = Column(String)
    sallary = Column(Integer)