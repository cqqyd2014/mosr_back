#encoding:utf-8
#数据库初始化
import datetime
import uuid
import click
from flask import current_app, g
from flask.cli import with_appcontext

from flaskr import db
#from .orm_session import create_session,_create_db_table
from .orm import *
#from net_tyc.database import *
#from bank.database import *
import platform
from python_common.selenium_common import init_database_system_par
#from python_common.database_common import base_system_code

from bank.database.initdb_sub import sub_run as bank_sub_run
from system.database.initdb_sub import sub_run as system_sub_run


def init_db(db_session):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db_session.commit()
    '''
    

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


    db_session.commit()

    '''
    #加载其他分项的初始化数据
    bank_sub_run(db_session)
    system_sub_run(db_session)



@click.command('init-db')
@with_appcontext
def init_db_command():
    db_session=db.get_flask_db()
    click.echo('Initialized the database start.')
    init_db(db_session)
    click.echo('Initialized the database compelet.')



def init_app(app):
    app.teardown_appcontext(db.close_flask_db)
    app.cli.add_command(init_db_command)
