
#encoding=utf-8
import os
from database import get_db,SystemPar,SystemCode,ProcessDetail,QueryTemplate,JobQueue,ImportData
import datetime
import platform
import time
from .opendb_getjob import opendb_getjob

def clean_neo4j():
    opendb_getjob('clean_neo4j',job)

def job(db_session,queue,current):

    system_type=''
    if platform.platform().find('Windows')>=0:
        system_type='Windows'
    else:
        system_type='UNIX'
    import_neo4j_install_dir=db_session.query(SystemPar).filter(SystemPar.par_code=='import_neo4j_install_dir').one()
    while True:
        if system_type=='Windows':
            windows_path=import_neo4j_install_dir.par_value.replace("/", "\\")
            if os.path.exists(windows_path+'data\\databases\\graph.db\\temp.db\\temp.db'):
                del_db_command='del /q '+windows_path+'data\\databases\\graph.db\\temp.db\\temp.db'
                r_del_db_command = os.popen(del_db_command).read()
            if os.path.exists(windows_path+'data\\databases\\graph.db\\temp.db'):
                del_db_command='del /q '+windows_path+'data\\databases\\graph.db\\temp.db'
                r_del_db_command = os.popen(del_db_command).read()
            if os.path.exists(windows_path+'data\\databases\\graph.db\\index'):
                del_db_command='del /q '+windows_path+'data\\databases\\graph.db\\index'
                r_del_db_command = os.popen(del_db_command).read()
            if os.path.exists(windows_path+'data\\databases\\graph.db\\profiles'):
                del_db_command='del /q '+windows_path+'data\\databases\\graph.db\\profiles'
                r_del_db_command = os.popen(del_db_command).read()
            if os.path.exists(windows_path+'data\\databases\\graph.db'):
                del_db_command='del /q '+windows_path+'data\\databases\\graph.db'
                r_del_db_command = os.popen(del_db_command).read()
            #删除目录
            if os.path.exists(windows_path+'data\\databases\\graph.db\\temp.db\\temp.db'):
                del_db_command='rd '+windows_path+'data\\databases\\graph.db\\temp.db\\temp.db'
                r_del_db_command = os.popen(del_db_command).read()
            if os.path.exists(windows_path+'data\\databases\\graph.db\\temp.db'):
                del_db_command='rd '+windows_path+'data\\databases\\graph.db\\temp.db'
                r_del_db_command = os.popen(del_db_command).read()
            if os.path.exists(windows_path+'data\\databases\\graph.db\\index'):
                del_db_command='rd '+windows_path+'data\\databases\\graph.db\\index'
                r_del_db_command = os.popen(del_db_command).read()
            if os.path.exists(windows_path+'data\\databases\\graph.db\\profiles'):
                del_db_command='rd '+windows_path+'data\\databases\\graph.db\\profiles'
                r_del_db_command = os.popen(del_db_command).read()
            if os.path.exists(windows_path+'data\\databases\\graph.db'):
                del_db_command='rd '+windows_path+'data\\databases\\graph.db'
                r_del_db_command = os.popen(del_db_command).read()
            #print("删除结束")
            #测试是否删掉
            if os.path.exists(windows_path+'data\\databases\\graph.db'):
                #数据库并未停止继续删除
                pass
            else:
                #print("tingzhi")
                break

        else:
            del_db_command='rm -Rf '+import_neo4j_install_dir.par_value+'data/databases/graph.db'
            r_del_db_command = os.popen(del_db_command).read()
            #测试是否删掉
            if os.path.exists(import_neo4j_install_dir.par_value+'data/databases/graph.db'):
                #数据库并未停止继续删除
                pass
            else:
                break
        time.sleep(10)
    current=datetime.datetime.now()
    return current