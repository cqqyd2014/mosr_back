
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class CompanyShareholderInfo(Base):
    __tablename__ = "company_shareholder_info"
    c_shareholder_name=Column(String(512))
    c_shareholder_id=Column(String(512), primary_key=True)
    c_shareholder_percent=Column(Numeric)
    c_shareholder_amount=Column(Numeric)
    c_shareholder_type=Column(String(64))#company#human
    c_company_id=Column(String(64), primary_key=True)
    c_company_name=Column(String(512))
    c_company_type=Column(String(64))

    
    def saveOrUpdate(self, session):
        db_data = session.query(CompanyShareholderInfo).filter(
            CompanyShareholderInfo.c_company_id == '',CompanyShareholderInfo.c_shareholder_id=='').one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.c_shareholder_name=self.c_shareholder_name
            db_data.c_shareholder_percent=self.c_shareholder_percent
            db_data.c_shareholder_amount=self.c_shareholder_amount
            db_data.c_company_id=self.c_company_id
            db_data.c_shareholder_type=self.c_shareholder_type
            db_data.c_company_name=self.c_company_name
            db_data.c_company_type=self.c_company_type



    @staticmethod
    def delete_all(db_session):
        db_session.query(CompanyShareholderInfo).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.c_company_id+self.c_shareholder_id

    def to_json(self):
        json_string = {
            'c_company_id': self.c_company_id,
            'c_shareholder_id': self.c_shareholder_id,
            'c_shareholder_name':self.c_shareholder_name,
            'c_shareholder_percent':self.c_shareholder_percent,
            'c_shareholder_amount': self.c_shareholder_amount,
            'c_shareholder_type':self.c_shareholder_type,
            'c_company_name':self.c_company_name,
            'c_company_type':self.c_company_type,

        }
        return json_string