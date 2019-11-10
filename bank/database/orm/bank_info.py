import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric,Float



class BankInfo(Base):
    __tablename__ = "bank_info"
    bank_code=Column(String(1024),primary_key=True)
    bank_name=Column(String(1024))
    

    def relSaveOrUpdate(self, session):
        db_data = session.query(BankInfo).filter(
            BankInfo.bank_no == self.bank_no).one_or_none()
        if db_data == None:
            session.add(self)
    
    def mainSaveOrUpdate(self, session):
        db_data = session.query(BankInfo).filter(
            BankInfo.bank_no == self.bank_no).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.bank_name=self.bank_name
            



    @staticmethod
    def delete_all(db_session):
        db_session.query(BankInfo).delete()
        #print("删除成功")


    def __repr__(self):
        return self.bank_no+'/'+self.bank_name

    def to_json(self):
        json_string = {
            'bank_no': self.bank_no,
            'bank_name': self.bank_name,
            

            

        }
        return json_string