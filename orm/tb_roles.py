'''
Created on 2020年2月20日

@author: xywl2019

用户表：用户基本信息
'''


from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class Roles(Base):
    '''
    classdocs
    '''
    __tablename__ = "roles"
    r_uuid = Column(String(37), primary_key=True)
    r_role_name     = Column(String(128), nullable=False,unique=True)
    r_memo = Column(Text)

    

