'''
Created on 2020年2月20日

@author: xywl2019

模块：数据库管道字段，所涉及数据的字段信息
'''
import uuid,datetime

from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class DatabasePipeCols(Base):
    '''
    classdocs
    '''
    __tablename__ = "database_pipe_cols"
    p_uuid = Column(String(36), primary_key=True)
    p_index     = Column(Integer(),primary_key=True)
    p_col_name=Column(String(512))
    p_col_alias=Column(String(512))
    last_modified=Column(DateTime,default=datetime.datetime.now)
    e_tag=Column(String(36),default=str(uuid.uuid1()))