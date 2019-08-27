# -*- coding: utf-8 -*-  
import platform

import datetime
import uuid
import json

from python_common.common import DateTimeEncoder
from .orm import *


postgresql_conn_str = "postgresql+psycopg2://mosr:Wang1980@localhost:33133/mosr"
engine = create_engine(postgresql_conn_str, isolation_level = 'READ COMMITTED',pool_size=10)

# mysql_conn_str='mysql+mysqldb://root:Wang1980@localhost:3306/mosr?charset=utf8mb4'
# engine=create_engine(mysql_conn_str)




def _create_db_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



def create_session():

    Session = sessionmaker(bind=engine)
    session = Session()

    return session






