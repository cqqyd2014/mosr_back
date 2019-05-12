from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Numeric,Float,Text,Date
import datetime


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

    @staticmethod
    def delete_all(db_session):
        db_session.query(SystemCode).delete()

#F10基本信息
class F10(Base):
    __tablename__ = "f10"
    f_market = Column(String(32),primary_key=True) # 沪A、深A
    f_code = Column(String(16),primary_key=True)
    f_name = Column(String(32))
    f_main_job=Column(String(512))
    f_trade=Column(String(128))
    f_last_updatetime=Column(DateTime)
    f_dynamic_pe=Column(Float)
    f_profit_per=Column(Float)
    f_capital_reserves=Column(Float)
    f_classification=Column(String(128))
    f_static_pe=Column(Float)
    f_undistributed_profits=Column(Float)
    f_capital=Column(Float)
    f_net_assets=Column(Float)
    f_earning_rate_net_assets=Column(Float)
    f_rate_gross=Column(Float)
    f_circulation_a=Column(Float)
    f_pb=Column(Float)

    def saveOfUpdate(self,session):
        f10_db = session.query(F10).filter(F10.f_market==self.f_market,F10.f_code==self.f_code).one_or_none()
        if f10_db==None:
            session.add(self)
        else:
            f10_db.f_name=self.f_name
            f10_db.f_main_job=self.f_main_job
            f10_db.f_trade=self.f_trade
            f10_db.f_last_updatetime=self.f_last_updatetime
            f10_db.f_dynamic_pe=self.f_dynamic_pe
            f10_db.f_profit_per=self.f_profit_per
            f10_db.f_capital_reserves=self.f_capital_reserves
            f10_db.f_classification=self.f_classification
            f10_db.f_static_pe=self.f_static_pe
            f10_db.f_undistributed_profits=self.f_undistributed_profits
            f10_db.f_capital=self.f_capital
            f10_db.f_net_assets=self.f_net_assets
            f10_db.f_earning_rate_net_assets=self.f_earning_rate_net_assets
            f10_db.f_rate_gross=self.f_rate_gross
            f10_db.f_circulation_a=self.f_circulation_a
            f10_db.f_pb=self.f_pb


def _create_db_table():
    Base.metadata.create_all(engine)

def create_session():
    _create_db_table()
    Session = sessionmaker(bind=engine)
    session = Session()
   
    return session

def init_db(db_session):
    SystemPar.delete_all(db_session)
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
    db_session.commit()
