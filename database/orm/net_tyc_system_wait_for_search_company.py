
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


# 当前等待导入的数据
class NetTycSystemWaitForSearchCompany(Base):
    __tablename__ = "net_tyc_system_wait_for_search_company"
    u_uuid = Column(String(37), primary_key=True)
    u_create_datetime = Column(DateTime)
    u_company_name = Column(String(512))
    u_start_search_datetime = Column(DateTime)
    u_end_search_datetime = Column(DateTime)
    u_status = Column(String(16))#准备、开始查询、查询出错、查询完毕、已删除
    
    @staticmethod
    def saveOfUpdate(self, session):
        db_data = session.query(NetTycSystemWaitForSearchCompany).filter(
            NetTycSystemWaitForSearchCompany.u_uuid == self.u_uuid).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.u_create_datetime = self.u_create_datetime
            db_data.u_company_name = self.u_company_name
            db_data.u_start_search_datetime = self.u_start_search_datetime
            db_data.u_end_search_datetime = self.u_end_search_datetime
            db_data.u_status=self.u_status

    @staticmethod
    def delete_all(db_session):
        db_session.query(NetTycSystemWaitForSearchCompany).delete()

    def __repr__(self):
        return self.u_uuid+self.u_declare_key+self.u_body

    def to_json(self):
        json_string = {
            'u_uuid': self.u_uuid,
            'u_create_datetime': json.dumps(self.u_create_datetime, cls=DateTimeEncoder),
            'u_company_name': self.u_company_name,
            'u_start_search_datetime': json.dumps(self.u_start_search_datetime, cls=DateTimeEncoder),
            'u_end_search_datetime': json.dumps(self.u_end_search_datetime, cls=DateTimeEncoder),
            
            'u_status': self.u_status,
          

        }
        return json_string