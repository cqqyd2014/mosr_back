'''
Created on 2020年2月20日

@author: xywl2019

模块：数据库管道，用于定义抽取数据，将数据对应到预定义模型，查看进度
'''
import uuid,datetime

from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class DatabasePipe(Base):
    '''
    classdocs
    '''
    __tablename__ = "database_pipe"
    p_uuid = Column(String(36), primary_key=True)
    p_name=Column(String(512))
    p_data_link_uuid     = Column(String(36))
    p_data_link_alias_name=Column(String(512))
    p_table_name=Column(String(512))
    p_source_type=Column(String(32))#'Table','SQL'
    p_source_sql=Column(String(2048))
    last_modified=Column(DateTime,default=datetime.datetime.now)
    e_tag=Column(String(36),default=str(uuid.uuid1()))
    is_delete=Column(Boolean)
    p_add_datetime=Column(DateTime)
    


    

