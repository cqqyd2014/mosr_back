'''
Created on 2020年2月20日

@author: xywl2019

Neo4j服务器状态
'''

from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class Neo4jServerStatus(object):
    '''
    classdocs
    '''


    __tablename__ = "neo4j_server_status"
    n_uuid = Column(String(37), primary_key=True)
    n_ip     = Column(String(128), nullable=False,unique=True)
    n_hostname = Column(String(128), nullable=False,unique=True)
    n_nickname=Column(String(128))
    n_addd_datetime=Column(DateTime)
    n_memo = Column(Text)