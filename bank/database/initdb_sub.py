#encoding:utf-8
#数据库初始化
import datetime
import uuid
import click
from flask import current_app, g
from flask.cli import with_appcontext

from flaskr import db
#from .orm_session import create_session,_create_db_table
from bank.database.orm import BankInfo
from net_tyc.database import *
import platform
from python_common.selenium_common import init_database_system_par
from python_common.database_common import base_system_code


def sub_run(db_session):
    BankInfo.delete_all(db_session)
    db_session.commit()
    bankInfo=BankInfo(bank_code='PSBC',bank_name='中国邮政储蓄银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CCB',bank_name='中国建设银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='ABC',bank_name='中国农业银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='ICBC',bank_name='中国工商银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='BOC',bank_name='中国银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CMBC',bank_name='中国民生银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CMB',bank_name='招商银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CIB',bank_name='兴业银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='BOB',bank_name='北京银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='BCM',bank_name='交通银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CEB',bank_name='中国光大银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CITIC',bank_name='中信银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='HXBANK',bank_name='华夏银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='GDB',bank_name='广发银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='SPDB',bank_name='浦东发展银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='EGBANK',bank_name='恒丰银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CZBANK',bank_name='浙商银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='HSBC',bank_name='汇丰银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='SDB',bank_name='深圳发展银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='BCQ',bank_name='重庆银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CQTGB',bank_name='重庆三峡银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='CQRCB',bank_name='重庆农村商业银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='PAB',bank_name='平安银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='HRB',bank_name='哈尔滨银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='BOCB',bank_name='成都银行')
    db_session.add(bankInfo)
    bankInfo=BankInfo(bank_code='SCB',bank_name='渣打银行')
    db_session.add(bankInfo)
    



    db_session.commit()


