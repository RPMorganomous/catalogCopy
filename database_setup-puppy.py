import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(80))
    zipCode = Column(String(20))
    website = Column(String(80))

class Puppy(Base):
    __tablename__ = 'puppy'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    date_of_birth = Column(Date)
    gender = Column(String(8))
    weight = Column(Integer)
    shelter_id = Column(Integer,ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    picture = Column(String(250))


engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)