import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric



class NetTycHumanBaseInfo(Base):
    __tablename__ = "net_tyc_human_base_info"
    h_human_id=Column(String(64),primary_key=True)
    h_human_name=Column(String(128))
    h_human_idcard=Column(String(18))
    h_tianyancha_link=Column(String(1024))
    h_memo=Column(Text)

    
    def relSaveOrUpdate(self, session):
        db_data = session.query(HumanBaseInfo).filter(
            HumanBaseInfo.h_human_id == self.h_human_id).one_or_none()
        if db_data == None:
            session.add(self)


    def mainSaveOrUpdate(self, session):
        db_data = session.query(HumanBaseInfo).filter(
            HumanBaseInfo.h_human_id == self.h_human_id).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.h_human_name=self.h_human_name
            db_data.h_human_idcard=self.h_human_idcard
            db_data.h_tianyancha_link=self.h_tianyancha_link
            db_data.h_memo=self.h_memo
            


    @staticmethod
    def delete_all(db_session):
        db_session.query(HumanBaseInfo).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.h_human_name+self.h_human_name+'/'+self.h_human_id

    def to_json(self):
        json_string = {
            'h_human_id': self.h_human_id,
            'h_human_name': self.h_human_name,
            'h_human_idcard':self.h_human_idcard,
            'h_tianyancha_link':self.h_tianyancha_link,
            'h_memo':self.h_memo,
            
            

        }
        return json_string