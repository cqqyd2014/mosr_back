'''
Created on 2020年2月20日

@author: xywl2019

用户属于角色：用户与角色对应关系
'''


from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class UsersToRoles(Base):
    '''
    classdocs
    '''
    __tablename__ = "users_to_roles"
    r_uuid = Column(String(37), primary_key=True)
    u_uuid = Column(String(37), primary_key=True)

    


        