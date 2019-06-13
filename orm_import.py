
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Numeric,Float,Text,Date,Boolean
import datetime
import uuid
import json
from common import DateTimeEncoder


def create_import_session(db_type):
    postgresql_conn_str="postgresql+psycopg2://postgres:Wang1980@localhost:33133/test"
    engine=create_engine(postgresql_conn_str)
    Base = declarative_base()
    
    Session = sessionmaker(bind=engine)
    session = Session()
   
    return session