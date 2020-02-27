'''
Created on 2020年2月20日

@author: xywl2019

组权限表：组对应模块的权限，权限有三种，decline，general,super
'''


from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class RolesPermission(Base):
    '''
    classdocs
    '''
    __tablename__ = "roles_permission"
    r_role_uuid = Column(String(37), primary_key=True)
    r_module_uuid     = Column(String(37),primary_key=True)
    r_permission=Column(String(37))


    

