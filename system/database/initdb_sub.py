#encoding:utf-8
#数据库初始化
import datetime
import uuid
import hashlib


import click
from flask import current_app, g
from flask.cli import with_appcontext

from flaskr import db
#from .orm_session import create_session,_create_db_table
from system.database.orm import SystemPar,SystemCode,SystemUser

import platform



def sub_run(db_session):
    SystemPar.delete_all(db_session)
    SystemCode.delete_all(db_session)
    db_session.commit()
    system_type=''
    if platform.platform().find('Windows')>=0:
        system_type='Windows'
    elif platform.platform().find('Darwin')>=0:
        system_type='Mac'
    elif platform.platform().find('Linux')>=0:
        system_type='Linux'
    else:
        system_type=None
    #base_system_code(db_session,SystemCode)
    
    # 基础数据
    systemPar = SystemPar(par_code='version',
                          par_desc='版本信息', par_value='1.1', par_type=2)
    db_session.add(systemPar)
    systemPar = SystemPar(par_code='node_count',
                          par_desc='节点数量', par_value='0', par_type=1)
    db_session.add(systemPar)
    systemPar = SystemPar(par_code='edge_count',
                          par_desc='关系数量', par_value='0', par_type=1)
    db_session.add(systemPar)
    systemPar = SystemPar(par_code='polling_second',
                          par_desc='Queue轮询间隔秒数', par_value='5', par_type=1)
    db_session.add(systemPar)

    if system_type=='UNIX':
        systemPar = SystemPar(par_code='import_neo4j_install_dir', par_desc='数据导入NEO4J安装目录',
                          par_value='/u01/neo4j-enterprise-3.5.6/', par_type=2)
        db_session.add(systemPar)
    else:
        systemPar = SystemPar(par_code='import_neo4j_install_dir', par_desc='数据导入NEO4J安装目录',
                          par_value='D:/software/neo4j-enterprise-3.5.6/', par_type=2)
        db_session.add(systemPar)
    systemPar = SystemPar(par_code='download_batch', par_desc='从远程服务器下载数据的批量',
                          par_value='10000', par_type=1)
    db_session.add(systemPar)
    systemPar = SystemPar(par_code='csv_batch', par_desc='读取和写入csv的批量',
                          par_value='10000', par_type=1)
    db_session.add(systemPar)
    systemPar = SystemPar(par_code='neo4j_status', par_desc='NEO4J状态',
                          par_value='未知', par_type=2)  # 可以为未知、启动中，运行中、关闭中，已关闭
    db_session.add(systemPar)
    systemPar = SystemPar(par_code='import_status',
                          par_desc='导入状态', par_value='空闲', par_type=2)  # 空闲、导入中
    db_session.add(systemPar)
    systemPar = SystemPar(par_code='neo4j_last_import_datetime',
                          par_desc='NEO4J数据最后更新时间', par_value='2019-06-07 12:44:44.0000', par_type=4)
    db_session.add(systemPar)
    systemCode = SystemCode(code_main='process_type', code_desc='任务类型',
                            code_code='systest', code_value='系统测试', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='process_type', code_desc='任务类型',
                            code_code='basedataimport', code_value='基础数据采集', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='process_type', code_desc='任务类型',
                            code_code='customizedataimport', code_value='自定义数据采集', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='CNY', code_value='人民币元', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='HKD', code_value='港元', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='JPY', code_value='日圆', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='SUR', code_value='卢布', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='CAD', code_value='加元', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='USD', code_value='美元', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='AUD', code_value='澳大利亚元', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='NZD', code_value='新西兰元', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='currency', code_desc='货币',
                            code_code='SGD', code_value='新加坡元', code_type=2)
    db_session.add(systemCode)
    #加管理员用户
    administrator=SystemUser(user_uuid=uuid.uuid1(),user_name='Administrator'
                              ,user_desc_name='管理员',user_password='Wang1980',user_password_md5=hashlib.md5('Wang1980'.encode(encoding='UTF-8')).hexdigest())
    db_session.add(administrator)
    db_session.commit()



