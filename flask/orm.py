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





class SystemDataCorp(Base):
    __tablename__="system_data_corp"
    corp_uscc = Column(String(18),primary_key=True)
    corp_name = Column(String(128),unique=True)
    

    @staticmethod
    def delete_all(db_session):
        db_session.query(SystemDataCorp).all().delete()
    
    def __repr__(self):
        return self.corp_name
    
    def to_json(self):
        json_string={
            'corp_uscc':self.corp_uscc,
            'corp_name':self.corp_name,
            

        }
        return json_string

    @staticmethod
    def from_json(json_string):
        return SystemPar(corp_uscc=json_string.get('corp_uscc'),corp_name=json_string.get('corp_name'))


class SystemData(Base):
    __tablename__="system_data"
    sys_uuid = Column(String(37),primary_key=True)
    sys_name = Column(String(128),unique=True)
    sys_end_date=Column(Date)
    sys_count=Column(Integer) # 1为数字2为文本3为日期4为日期时间（含毫秒）

    @staticmethod
    def delete_all(db_session):
        db_session.query(SystemData).all().delete()
    
    def __repr__(self):
        return self.sys_name
    
    def to_json(self):
        json_string={
            'sys_uuid':self.sys_uuid,
            'sys_name':self.sys_name,
            'sys_end_date':json.dumps(self.sys_end_date,cls=DateTimeEncoder),
            'sys_count':self.sys_count

        }
        return json_string

    @staticmethod
    def from_json(json_string):
        return SystemPar(par_code=json_string.get('sys_uuid'),par_desc=json_string.get('sys_name'),par_value=json_string.get('sys_end_date'),par_type=json_string.get('sys_count'))

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
        
class NodeLabelColor(Base):
    __tablename__ = "node_label_color"
    n_lable_classs = Column(String(256),primary_key=True)
    n_color=Column(String(6))
    n_lable_display = Column(String(256),unique=True)
    

    def to_json(self):
        json_string={
            'n_lable_classs':self.n_lable_classs,
            'n_color':self.n_color,
            'n_display':self.n_display,
            

        }
        return json_string

    @staticmethod
    def delete_all(db_session):
        db_session.query(NodeLabelColor).all().delete()
    
    def saveOfUpdate(self,session):
        db_data = session.query(NodeLabelColor).filter(NodeLabelColor.n_lable_classs==self.n_lable_classs).one_or_none()
        if db_data==None:
            session.add(self)
        else:
            db_data.n_color=self.n_color
            db_data.n_display=self.n_display

            

class SystemCode(Base):
    __tablename__ = "system_code"
    code_main = Column(String(64),primary_key=True)
    code_desc = Column(String(256))
    code_code = Column(String(128),primary_key = True,unique=True)
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

class Neno4jCatalog(Base):
    __tablename__ = "neo4j_catlog"
    nc_uuid = Column(String(37),primary_key=True)
    nc_update_datetime = Column(DateTime)
    nc_type = Column(String(64))
    nc_value = Column(String(512))
    

    def to_json(self):
        
        json_string={
            'nc_uuid':self.nc_uuid,
            'nc_update_datetime':json.dumps(self.nc_update_datetime,cls=DateTimeEncoder),
            'nc_type':self.nc_type,
            'nc_value':self.nc_value,
           

        }
        
        
        return json_string

            

class QueryTemplate(Base):
    __tablename__ = "query_template"
    qt_uuid = Column(String(37),primary_key=True)
    qt_datetime = Column(DateTime)
    qt_object = Column(Text)
    qt_cypher = Column(Text)
    qt_title= Column(String(1024))
    qt_desc = Column(Text)

    def to_json(self):
        
        json_string={
            'qt_uuid':self.qt_uuid,
            'qt_datetime':json.dumps(self.qt_datetime,cls=DateTimeEncoder),
            'qt_object':self.qt_object,
            'qt_cypher':self.qt_cypher,
            'qt_title':self.qt_title,
            'qt_desc':self.qt_desc,

        }
        
        
        return json_string


class ProcessDetail(Base):
    __tablename__ = "process_detail"
    pd_uuid = Column(String(37),primary_key=True)
    pd_start_datetime = Column(DateTime)
    pd_catalog = Column(String(32),ForeignKey('system_code.code_code'))
    pd_command = Column(Text)


    def to_json(self):
        
        json_string={
            'pd_uuid':self.pd_uuid,
            'pd_start_datetime':json.dumps(self.pd_start_datetime,cls=DateTimeEncoder),
            'pd_catalog':self.pd_catalog,
            'pd_command':self.pd_command,

        }
        
        
        return json_string

    @staticmethod
    def delete_all(db_session):
        db_session.query(ProcessDetail).all().delete()
    
    def saveOfUpdate(self,session):
        db_data = session.query(ProcessDetail).filter(ProcessDetail.pd_uuid==self.pd_uuid).one_or_none()
        if db_data==None:
            session.add(self)
        else:
            db_data.pd_start_datetime=self.pd_start_datetime
            db_data.pd_catalog=self.pd_catalog
            db_data.pd_command=self.pd_command




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
    #节点色彩
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='FFFFCC',code_value='FFFFCC',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='CCFFFF',code_value='CCFFFF',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='FFCCCC',code_value='FFCCCC',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='CCCCFF',code_value='CCCCFF',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='99CCCC',code_value='99CCCC',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='99CCFF',code_value='99CCFF',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='CCCCCC',code_value='CCCCCC',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='CCCC99',code_value='CCCC99',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='3399CC',code_value='3399CC',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='FFCC99',code_value='FFCC99',code_type=2)
    db_session.add(systemCode)
    systemCode=SystemCode(code_main='node_color',code_desc='节点色彩',code_code='99CC33',code_value='99CC33',code_type=2)
    db_session.add(systemCode)
    

    #测试数据
    processDetail=ProcessDetail(pd_uuid=str(uuid.uuid1()),pd_start_datetime=datetime.datetime.now(),pd_catalog='systest',pd_command='SQL1Annotations are a concept used internally by SQLAlchemy in order to store additional information along with ClauseElement objects. A Python dictionary is associated with a copy of the object, which contains key/value pairs significant to various internal systems, mostly within the ORM:')
    db_session.add(processDetail)
    systemData=SystemData(sys_uuid=str(uuid.uuid1()),sys_name='统一社会编码的法人机构',sys_end_date=datetime.datetime.now(),sys_count=10000)
    db_session.add(systemData)
    systemData=SystemData(sys_uuid=str(uuid.uuid1()),sys_name='自然人',sys_end_date=datetime.datetime.now(),sys_count=30000)
    db_session.add(systemData)

    db_session.commit()
    print('init db ok')
