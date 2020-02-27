'''
Created on 2020年2月20日

@author: xywl2019

模块：系统模块，用于页面显示和模块挂载,type为两种，一种为module，一种为sub_module
submoule是有下级的情况
'''


from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class Modules(Base):
    '''
    classdocs
    '''
    __tablename__ = "modules"
    m_uuid = Column(String(37), primary_key=True)
    m_name     = Column(String(37),nullable=False,unique=True)
    m_route_url=Column(String(256))
    m_type=Column(String(37))
    m_icon=Column(String(64))
    m_up_uuid=Column(String(37))
    m_level=Column(Integer)
    m_order=Column(Integer)


    

