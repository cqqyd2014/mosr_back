
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


class HumanLawman(Base):
    __tablename__ = "human_lawman"
    h_human_id=Column(String(64),primary_key=True)
    h_human_name=Column(String(256))
    c_company_id=Column(String(64),primary_key=True)
    c_company_name=Column(String(256))
    c_company_type=Column(String(256))
    

    
    def saveOrUpdate(self, session):
        db_data = session.query(HumanLawman).filter(
            HumanLawman.h_human_id == self.h_human_id,HumanLawman.c_company_id == self.c_company_id).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.c_company_name=self.c_company_name
            db_data.c_company_type=self.c_company_type
            db_data.h_human_name=self.h_human_name
            


    @staticmethod
    def delete_all(db_session):
        db_session.query(HumanLawman).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.h_human_id+self.c_company_id

    def to_json(self):
        json_string = {
            'h_human_id': self.h_human_id,
            'c_company_id': self.c_company_id,
            'c_company_name':self.c_company_name,
            'c_company_type':self.c_company_type,
            'h_human_name':self.h_human_name
            
            
            

        }
        return json_string