'''
Created on 2020年2月19日

@author: xywl2019
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Float, Text, Date, Boolean
import uuid
import datetime
from _datetime import date
Base = declarative_base()


import configparser
conf = configparser.ConfigParser()
conf.sections()
conf.read('db_config.ini')
db_url=conf['Database']["Db_url"]
engine = create_engine(db_url, isolation_level = 'READ COMMITTED',pool_size=10,echo=True)


    
from .tb_users import Users
from .tb_roles import Roles
from .tb_users_to_roles import UsersToRoles
from .tb_system_parameters import SystemParameters
from .tb_roles import Roles
from .tb_users_to_roles import UsersToRoles
from .tb_module import Modules
from .tb_role_permission import RolesPermission
from .tb_module import Modules
from .tb_neo4j_server_status import Neo4jServerStatus
from .tb_database_link import DatabaseLink
from .tb_database_pipe import DatabasePipe


def get_db():
    
    Session = sessionmaker(bind=engine)
    session = Session()
        

    return session


def init_db(db_session):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    #db_session.commit()
    now=datetime.datetime.now()
    #新建两个用户，分别是admin和xywl2019
    admin=Users(u_uuid='d7bd1f5d-bc1e-4cc0-8881-2c7a61992f55',u_user_name='admin',u_user_password='123456cq',u_effective=True,u_nickname='管理员',last_modified=datetime.datetime.now(),e_tag=str(uuid.uuid1()))
    xywl2019=Users(u_uuid='c1368fcb-7b00-4e47-ba70-514da603fc66',u_user_name='xywl2019',u_user_password='123456cq',u_effective=True,u_nickname='夏花',last_modified=datetime.datetime.now(),e_tag=str(uuid.uuid1()))
    #指定版本
    sp_version=SystemParameters(s_param='version',s_value='1.1',s_desc='系统版本')
    #新建两个角色
    admin_role=Roles(r_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_role_name='admins')
    users_role=Roles(r_uuid='554b6ea5-d971-4f4f-af25-aafda153a137',r_role_name='users')
    #将两个用户加入组
    add_admin_to_admins=UsersToRoles(r_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',u_uuid='d7bd1f5d-bc1e-4cc0-8881-2c7a61992f55')
    add_xywl2019_to_users=UsersToRoles(r_uuid='554b6ea5-d971-4f4f-af25-aafda153a137',u_uuid='c1368fcb-7b00-4e47-ba70-514da603fc66')
    #新建系统模块
    m_homepage=Modules(m_level=1,m_order=1,m_uuid='5bc13e30-37f9-4edf-82d5-8f50555d3bbb',m_name='主页',m_route_url='/home',m_type='module',m_icon='home')
    m_system_manage=Modules(m_level=1,m_order=2,m_uuid='c1151e32-fa8e-44cd-bb06-03c6950109ce',m_name='系统管理',m_route_url='/system_manage',m_type='sub_module',m_icon='control')
    m_team_manage=Modules(m_level=2,m_order=3,m_uuid='04d7d7d9-7673-4dfe-bc21-4e8558631fe6',m_name='组队管理',m_route_url='/team_manage',m_type='module',m_icon='team',m_up_uuid='c1151e32-fa8e-44cd-bb06-03c6950109ce')
    m_user_manage=Modules(m_level=2,m_order=4,m_uuid='4e1bd281-2bf9-491f-b3de-61a956ba957a',m_name='用户管理',m_route_url='/user_manage',m_type='module',m_icon='user',m_up_uuid='c1151e32-fa8e-44cd-bb06-03c6950109ce')
    m_data_manage=Modules(m_level=1,m_order=5,m_uuid='4dc914ac-9343-44fb-a16f-e0715c639801',m_name='数据管理',m_route_url='/data_manage',m_type='sub_module',m_icon='database')
    m_data_link=Modules(m_level=2,m_order=6,m_uuid='a5f0af00-198e-4536-955c-4067de05fc80',m_name='数据源',m_route_url='/database_links',m_type='module',m_icon='database',m_up_uuid='4dc914ac-9343-44fb-a16f-e0715c639801')
    m_data_pipe=Modules(m_level=2,m_order=7,m_uuid='6e3cf278-cb4f-48ad-90ed-6cc2d926ba17',m_name='数据管道',m_route_url='/database_pipes',m_type='module',m_icon='database',m_up_uuid='4dc914ac-9343-44fb-a16f-e0715c639801')
    m_data_hbase_info=Modules(m_level=2,m_order=8,m_uuid='bc75b9af-fb59-44af-8328-e2446ea04bf0',m_name='Hbase监控',m_route_url='/database_hbase_info',m_type='module',m_icon='database',m_up_uuid='4dc914ac-9343-44fb-a16f-e0715c639801')
    #分配权限，uers组对于大多数人，admin组为管理员，
    #1、为admin组分配首页、组队、用户管理权限的权限，不考虑机构设置
    permit_admin_home=RolesPermission(r_role_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_module_uuid='5bc13e30-37f9-4edf-82d5-8f50555d3bbb',r_permission='general')
    permit_admin_system=RolesPermission(r_role_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_module_uuid='c1151e32-fa8e-44cd-bb06-03c6950109ce',r_permission='general')
    permit_admin_team_manage=RolesPermission(r_role_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_module_uuid='04d7d7d9-7673-4dfe-bc21-4e8558631fe6',r_permission='general')
    permit_admin_user_manage=RolesPermission(r_role_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_module_uuid='4e1bd281-2bf9-491f-b3de-61a956ba957a',r_permission='general')
    permit_admin_data_manage=RolesPermission(r_role_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_module_uuid='4dc914ac-9343-44fb-a16f-e0715c639801',r_permission='general')
    permit_admin_data_link=RolesPermission(r_role_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_module_uuid='a5f0af00-198e-4536-955c-4067de05fc80',r_permission='general')
    permit_admin_data_pipe=RolesPermission(r_role_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_module_uuid='6e3cf278-cb4f-48ad-90ed-6cc2d926ba17',r_permission='general')
    permit_admin_data_hbase_info=RolesPermission(r_role_uuid='79923c4b-37f2-4e9b-abf5-09ecdaec86db',r_module_uuid='bc75b9af-fb59-44af-8328-e2446ea04bf0',r_permission='general')
    #2、为user分配权限
    #数据联接信息
    databaseLink=DatabaseLink(d_alias='Test',d_uuid='297bc565-6b95-49c4-858a-e27ce23e8c1e',d_type='MS SQLSERVER',d_ip='192.168.88.46',d_port='1433',d_db_name='sbdet',d_user_name='sa',d_password='Wang1980',d_memo='测试',d_add_datetime=datetime.datetime.now(),d_add_username='admin',last_modified=datetime.datetime.now(),e_tag=str(uuid.uuid1()),is_delete=False)
    #数据通道信息
    databasePipe=DatabasePipe(p_name='测试通道',p_uuid='8fe9caa7-43c7-4fcb-9aaf-7f95ccdc5189',p_data_link_uuid='297bc565-6b95-49c4-858a-e27ce23e8c1e',p_data_link_alias_name='Test',p_table_name='a',p_source_type='Table',p_source_sql='select * from table',last_modified=datetime.datetime.now(),e_tag='09847f70-5aec-4f5e-8217-42b376b5b126',is_delete=False,p_add_datetime=datetime.datetime.now())
    
    db_session.add_all([databasePipe,permit_admin_data_hbase_info,m_data_hbase_info,m_data_pipe,permit_admin_data_pipe,databaseLink,permit_admin_data_link,permit_admin_data_manage,m_data_link,m_data_manage,permit_admin_system,permit_admin_home,permit_admin_user_manage,permit_admin_team_manage,admin,sp_version,admin_role,add_admin_to_admins,xywl2019,users_role,add_xywl2019_to_users,m_homepage,m_system_manage,m_team_manage,m_user_manage])
    db_session.commit()
