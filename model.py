from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import JSON, Integer, Column, String, ARRAY
import os
from dotenv import load_dotenv
load_dotenv()
PG_DSN = 'postgresql+asyncpg://%s:%s@127.0.0.1:5432/%s' % \
         (os.getenv('NAME'), os.getenv('PASSWORD'), os.getenv('DATABASE'))
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class SwapiPeople(Base):

    __tablename__ = 'swapi_people'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    birth_year = Column(String(length=100))
    eye_color = Column(String(length=100))
    gender = Column(String(length=100))
    hair_color = Column(String(length=100))
    height = Column(String(length=100))
    mass = Column(String(length=100))
    skin_color = Column(String(length=100))
    homeworld = Column(ARRAY(String))
    films = Column(ARRAY(String))
    species = Column(ARRAY(String))
    starships = Column(ARRAY(String))
    vehicles = Column(ARRAY(String))

