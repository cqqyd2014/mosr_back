
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


class NetTycJobDetail(Base):
    __tablename__ = "net_tyc_job_detail"
    j_uuid=Column(String(37),primary_key=True)
    j_detail_uuid=Column(String(37),primary_key=True)
    j_text=Column(String(512))
    j_search_type=Column(String(256))#'single_company','single_human'
    j_search_status=Column(String(64))#'发布','处理中','完成','出错','已删除'
    j_result=Column(Text)
    j_search_start_datetime=Column(DateTime)
    j_search_end_datetime=Column(DateTime)
    

    
    def saveOrUpdate(self, session):
        db_data = session.query(NetTycJobDetail).filter(
            NetTycJobDetail.j_uuid == self.j_uuid,NetTycJobDetail.j_detail_uuid == self.j_detail_uuid).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.j_text=self.j_text
            db_data.c_company_type=self.c_company_type
            db_data.j_search_type=self.j_search_type
            db_data.j_search_status=self.j_search_status
            db_data.j_result=self.j_result
            db_data.j_search_start_datetime=self.j_search_start_datetime
            db_data.j_search_end_datetime=self.j_search_end_datetime
            
            


    @staticmethod
    def delete_all(db_session):
        db_session.query(NetTycJobDetail).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.j_uuid+self.j_detail_uuid

    def to_json(self):
        json_string = {
            'j_uuid': self.j_uuid,
            'j_detail_uuid': self.j_detail_uuid,
            'j_text':self.j_text,
            'j_search_type':self.j_search_type,
            'j_search_status':self.j_search_status
            
            
            

        }
        return json_string