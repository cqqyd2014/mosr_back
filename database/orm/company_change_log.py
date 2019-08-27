

import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date

class CompanyChangeLog(Base):
    __tablename__ = "compnay_change_log"
    c_change_order=Column(Integer, primary_key=True)
    c_change_date=Column(Date)
    c_change_item=Column(String(512))

    c_change_before=Column(Text)
    c_change_after=Column(Text)

    c_company_id=Column(String(64), primary_key=True)

    
    def saveOfUpdate(self, session):
        db_data = session.query(CompanyChangeLog).filter(
            CompanyChangeLog.c_company_id == self.c_company_id,CompanyChangeLog.c_change_order==self.c_change_order).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.c_change_date=self.c_change_date
            db_data.c_change_item=self.c_change_item
            db_data.c_change_before=self.c_change_before
            db_data.c_change_after=self.c_change_after
            



    @staticmethod
    def delete_all(db_session):
        db_session.query(CompanyChangeLog).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.c_company_id+self.c_change_order

    def to_json(self):
        json_string = {
            'c_company_id': self.c_company_id,
            'c_change_order': self.c_change_order,
            'c_change_date':json.dumps(self.c_change_date, cls=DateTimeEncoder),
            'c_change_item':self.c_change_item,
            'c_change_before':self.c_change_before,
            'c_change_after': self.c_change_after,
            

        }
        return json_string