#encoding:utf-8
#数据库初始化
import datetime
import uuid

from .orm_session import create_session,_create_db_table
from .orm import SystemPar,SystemCode,ProcessDetail
import platform
from python_common.selenium_common import init_database_system_par
from python_common.database_common import base_system_code


def init_db(db_session):
    _create_db_table()
    db_session.commit()
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
    base_system_code(db_session,SystemCode)
    init_database_system_par(system_type,db_session,SystemPar)
    # 基础数据
    systemPar = SystemPar(par_code='version',
                          par_desc='版本信息', par_value='1.0', par_type=2)
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
                          par_value='/u01/cqaudit/software/neo4j-enterprise-3.5.6/', par_type=2)
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
    # 节点色彩
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='FFFFCC', code_value='FFFFCC', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='CCFFFF', code_value='CCFFFF', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='FFCCCC', code_value='FFCCCC', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='CCCCFF', code_value='CCCCFF', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='99CCCC', code_value='99CCCC', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='99CCFF', code_value='99CCFF', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='CCCCCC', code_value='CCCCCC', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='CCCC99', code_value='CCCC99', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='3399CC', code_value='3399CC', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='FFCC99', code_value='FFCC99', code_type=2)
    db_session.add(systemCode)
    systemCode = SystemCode(code_main='node_color', code_desc='节点色彩',
                            code_code='99CC33', code_value='99CC33', code_type=2)
    db_session.add(systemCode)
     # 测试数据
    processDetail = ProcessDetail(pd_uuid=str(uuid.uuid1()), pd_start_datetime=datetime.datetime.now(), pd_catalog='systest',
                                  pd_command='SQL1Annotations are a concept used internally by SQLAlchemy in order to store additional information along with ClauseElement objects. A Python dictionary is associated with a copy of the object, which contains key/value pairs significant to various internal systems, mostly within the ORM:')
    db_session.add(processDetail)

    db_session.commit()
    print('init db ok！')


def main():
    db_session=create_session()
    init_db(db_session)
    db_session.close()
    

if __name__ == '__main__':
    main()