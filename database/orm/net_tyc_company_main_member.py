
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class NetTycCompanyMainMember(Base):
    __tablename__ = "net_tyc_compnay_main_member"

    c_member_id=Column(String(512), primary_key=True)
    c_member_href=Column(String(1024))
    c_member_type=Column(String(512))
    c_member_job=Column(String(512), primary_key=True)
    c_member_name=Column(String(512))

    c_company_id=Column(String(64), primary_key=True)
    c_company_name=Column(String(512))

    
    def saveOrUpdate(self, session):
        db_data = session.query(CompanyMainMember).filter(
            CompanyMainMember.c_company_id == self.c_company_id,CompanyMainMember.c_member_id==self.c_member_id,CompanyMainMember.c_member_job==self.c_member_job).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.c_member_href=self.c_member_href
            db_data.c_member_type=self.c_member_type
            db_data.c_member_name=self.c_member_name
            db_data.c_company_name=self.c_company_name
            
            



    @staticmethod
    def delete_all(db_session):
        db_session.query(CompanyMainMember).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.c_company_id+self.c_member_id+self.c_member_job

    def to_json(self):
        json_string = {
            'c_member_id': self.c_member_id,
            'c_member_href': self.c_member_href,
            'c_member_type':self.c_member_type,
            'c_member_job':self.c_member_job,
            'c_member_name':self.c_member_name,
            'c_company_id': self.c_company_id,
            'c_company_name': self.c_company_name,
            

        }
        return json_string