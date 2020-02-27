'''
Created on 2020年2月20日

@author: xywl2019

角色表：角色基本信息
'''

import datetime,uuid
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class Users(Base):
    '''
    classdocs
    '''
    __tablename__ = "users"
    u_uuid = Column(String(37), primary_key=True)
    u_user_name     = Column(String(128), nullable=False,unique=True)
    u_user_password     = Column(String(128), nullable=False)
    u_nickname=Column(String(128), nullable=False)
    u_effective = Column(Boolean, nullable=False)
    u_memo = Column(Text)
    u_last_login_datetime=Column(DateTime)
    
    last_modified=Column(DateTime,default=datetime.datetime.now)
    e_tag=Column(String(36),default=str(uuid.uuid1()))
    
    def __repr__(self):
        return self.u_uuid+self.u_user_name



        