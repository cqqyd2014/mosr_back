
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric

class CompanyBranch(Base):
    __tablename__ = "compnay_branch"

    c_branch_id=Column(String(512), primary_key=True)
    c_branch_name=Column(String(512))
    c_branch_type=Column(String(512))
    c_company_id=Column(String(64), primary_key=True)
    c_company_name=Column(String(512))
    c_company_type=Column(String(512))

    
    def saveOrUpdate(self, session):
        db_data = session.query(CompanyBranch).filter(
            CompanyBranch.c_company_id == self.c_company_id,CompanyBranch.c_branch_id==self.c_branch_id).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.c_branch_name=self.c_branch_name
            db_data.c_branch_type=self.c_branch_type
            db_data.c_company_name=self.c_company_name
            db_data.c_company_type=self.c_company_type

            
            



    @staticmethod
    def delete_all(db_session):
        db_session.query(CompanyBranch).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.c_company_id+self.c_branch_id

    def to_json(self):
        json_string = {
            'c_company_id': self.c_company_id,
            'c_branch_id': self.c_branch_id,
            'c_branch_name':self.c_branch_name,
            'c_branch_type':self.c_branch_type,
            'c_company_name':self.c_company_name,
            'c_company_type':self.c_company_type,

            

        }
        return json_string