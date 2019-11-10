import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric,Float



class BankOuterTradeDetail(Base):
    __tablename__ = "bank_outer_trade_detail"
    account_no=Column(String(1024),primary_key=True)
    account_name=Column(String(1024))
    card_no=Column(String(1024))
    trade_datetime=Column(DateTime,primary_key=True)
    trade_seq=Column(String(1024),primary_key=True)
    amount=Column(Float)
    banlance=Column(Float)
    trade_code=Column(String(1024))
    opp_bank_code=Column(String(1024))
    opp_bank_name=Column(String(1024))
    opp_account_no=Column(String(1024))
    opp_account_name=Column(String(1024))
    memo=Column(String(1024))
    bank_code=Column(String(1024),primary_key=True)
    

    def relSaveOrUpdate(self, session):
        db_data = session.query(BankOuterTradeDetail).filter(
            BankOuterTradeDetail.account_no == self.account_no
            ,BankOuterTradeDetail.trade_datetime == self.trade_datetime
            ,BankOuterTradeDetail.trade_seq == self.trade_seq
            ,BankOuterTradeDetail.bank_code == self.bank_code).one_or_none()
        if db_data == None:
            session.add(self)
    
    def mainSaveOrUpdate(self, session):
        db_data = session.query(BankOuterTradeDetail).filter(
           BankOuterTradeDetail.account_no == self.account_no
            ,BankOuterTradeDetail.trade_datetime == self.trade_datetime
            ,BankOuterTradeDetail.trade_seq == self.trade_seq
            ,BankOuterTradeDetail.bank_code == self.bank_code).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.account_name=self.account_name
            db_data.card_no=self.card_no
            db_data.amount=self.amount
            db_data.banlance=self.banlance
            db_data.trade_code=self.trade_code
            db_data.opp_bank_code=self.opp_bank_code
            db_data.opp_bank_name=self.opp_bank_name
            db_data.opp_account_no=self.opp_account_no
            db_data.opp_account_name=self.opp_account_name
            db_data.memo=self.memo
            



    @staticmethod
    def delete_all(db_session):
        db_session.query(BankOuterTradeDetail).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.account_no+'/'+self.trade_datetime+'/'+self.trade_seq+'/'+self.bank_code

    def to_json(self):
        json_string = {
            'account_no': self.account_no,
            'trade_datetime': self.trade_datetime,
            'trade_seq':self.trade_seq,
            'bank_code':self.bank_code,
            'account_name':self.account_name,
            'card_no': self.card_no,
            'amount': self.amount,
            'banlance': self.banlance,
            'trade_code': self.trade_code,
            'opp_bank_code': self.opp_bank_code,
            'opp_bank_name': self.opp_bank_name,
            'opp_account_no': self.opp_account_no,
            'opp_account_name':self.opp_account_name,
            'memo':self.memo

            

        }
        return json_string