from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Numeric,Float,Text,Date,Boolean
import datetime
import uuid
import json
from common import DateTimeEncoder


postgresql_conn_str="postgresql+psycopg2://postgres:Wang1980@localhost:33133/test"
engine=create_engine(postgresql_conn_str)
Base = declarative_base()

class SystemPar(Base):
    __tablename__="system_par"
    par_code = Column(String(64),primary_key=True)
    par_desc = Column(String(128))
    par_value=Column(String(1024))
    par_type=Column(Integer) # 1为数字2为文本3为日期4为日期时间（含毫秒）

    @staticmethod
    def delete_all(db_session):
        db_session.query(SystemPar).delete()
    
    def __repr__(self):
        return self.par_code+"_"+self.par_value
    
    def to_json(self):
        json_string={
            'par_code':self.par_code,
            'par_desc':self.par_desc,
            'par_value':self.par_value,
            'par_type':self.par_type

        }
        return json_string

    @staticmethod
    def from_json(json_string):
        return SystemPar(par_code=json_string.get('par_code'),par_desc=json_string.get('par_desc'),par_value=json_string.get('par_value'),par_type=json_string.get('par_type'))
        

class SystemCode(Base):
    __tablename__ = "system_code"
    code_main = Column(String(64),primary_key=True)
    code_desc = Column(String(256))
    code_code = Column(String(128),primary_key = True)
    code_value = Column(String(1024))
    code_type=Column(Integer) # 1为数字2为文本3为日期4为日期时间（含毫秒）

    def to_json(self):
        json_string={
            'code_main':self.code_main,
            'code_desc':self.code_desc,
            'code_code':self.code_code,
            'code_value':self.code_value,
            'code_type':self.code_type,

        }
        return json_string

    @staticmethod
    def delete_all(db_session):
        db_session.query(SystemCode).delete()
    
    def saveOfUpdate(self,session):
        db_data = session.query(SystemCode).filter(SystemCode.code_main==self.code_main,SystemCode.code_code==self.code_code).one_or_none()
        if db_data==None:
            session.add(self)
        else:
            db_data.code_desc=self.code_desc
            db_data.code_value=self.code_value
            db_data.f_trade=self.f_trade
            db_data.code_type=self.code_type
            

class ProcessDetail(Base):
    __tablename__ = "process_detail"
    pd_uuid = Column(String(37),primary_key=True)
    pd_start_datetime = Column(DateTime)
    pd_catalog = Column(String(32))
    pd_command = Column(Text)
    pd_end_datetime=Column(DateTime)
    pd_current_process=Column(Boolean)

    def to_json(self):
        
        json_string={
            'pd_uuid':self.pd_uuid,
            'pd_start_datetime':json.dumps(self.pd_start_datetime,cls=DateTimeEncoder),
            'pd_catalog':self.pd_catalog,
            'pd_command':self.pd_command,
            'pd_end_datetime':json.dumps(self.pd_end_datetime,cls=DateTimeEncoder),
            'pd_current_process':self.pd_current_process,

        }
        
        
        return json_string

    @staticmethod
    def delete_all(db_session):
        db_session.query(ProcessDetail).delete()
    
    def saveOfUpdate(self,session):
        db_data = session.query(ProcessDetail).filter(ProcessDetail.pd_uuid==self.pd_uuid).one_or_none()
        if db_data==None:
            session.add(self)
        else:
            db_data.pd_start_datetime=self.pd_start_datetime
            db_data.pd_catalog=self.pd_catalog
            db_data.pd_command=self.pd_command
            db_data.pd_end_datetime=self.pd_end_datetime
            db_data.pd_current_process=self.pd_current_process



def _create_db_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_session():
    
    Session = sessionmaker(bind=engine)
    session = Session()
   
    return session

def init_db(db_session):
    _create_db_table()
    SystemPar.delete_all(db_session)
    #基础数据
    systemPar=SystemPar(par_code='version',par_desc='版本信息',par_value='1.0',par_type=2)
    db_session.add(systemPar)
    SystemCode.delete_all(db_session)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='CNY',code_value='人民币元',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='HKD',code_value='港元',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='JPY',code_value='日圆',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='SUR',code_value='卢布',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='CAD',code_value='加元',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='USD',code_value='美元',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='AUD',code_value='澳大利亚元',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='NZD',code_value='新西兰元',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='currency',code_desc='货币',code_code='SGD',code_value='新加坡元',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='process_type',code_desc='任务类型',code_code='systest',code_value='系统测试',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='process_type',code_desc='任务类型',code_code='basedataimport',code_value='基础数据采集',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='process_type',code_desc='任务类型',code_code='customizedataimport',code_value='自定义数据采集',code_type=2)
    db_session.add(systemCode)
    #测试数据
    processDetail=ProcessDetail(pd_uuid=str(uuid.uuid1()),pd_start_datetime=datetime.datetime.now(),pd_catalog='systest',pd_command='SQL1',pd_end_datetime=datetime.datetime.now()+datetime.timedelta(days=1),pd_current_process=True)
    db_session.add(processDetail)
    db_session.commit()
    print('init db ok')
