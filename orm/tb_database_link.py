'''
Created on 2020年2月20日

@author: xywl2019

模块：数据库联接，用于存储访问远程数据库信息
'''
import uuid,datetime

from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class DatabaseLink(Base):
    '''
    classdocs
    '''
    __tablename__ = "database_link"
    d_uuid = Column(String(37), primary_key=True)
    d_type     = Column(String(32))
    d_ip=Column(String(256))
    d_port=Column(String(37))
    d_db_name=Column(String(128))
    d_user_name=Column(String(128))
    d_password=Column(String(128))
    d_memo=Column(Text)
    d_alias=Column(String(256))
    d_add_datetime=Column(DateTime)
    d_add_username=Column(String(128))
    d_url=Column(String(512))
    last_modified=Column(DateTime,default=datetime.datetime.now)
    e_tag=Column(String(36),default=str(uuid.uuid4()))
    is_delete=Column(Boolean)
    


    

