'''
Created on 2020年2月20日

@author: xywl2019

系统参数：系统参数
'''
import datetime,uuid

from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class SystemParameters(Base):
    '''
    classdocs
    '''
    __tablename__ = "system_parameters"
    s_param = Column(String(256), primary_key=True)
    s_value=Column(String(256))
    s_desc=Column(Text)
    last_modified=Column(DateTime,default=datetime.datetime.now)
    e_tag=Column(String(36),default=str(uuid.uuid1()))

    



        