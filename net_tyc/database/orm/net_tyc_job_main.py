
import json
from python_common.common import DateTimeEncoder
from database import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


class NetTycJobMain(Base):
    __tablename__ = "net_tyc_job_main"
    j_uuid=Column(String(37),primary_key=True)
    j_def_datetime=Column(DateTime)
    j_start_datetime=Column(DateTime)
    j_end_datetime=Column(DateTime)
    j_status=Column(String(32))#'发布','处理中','完成','出错','已删除'
    j_memo=Column(Text)
    

    
    def saveOrUpdate(self, session):
        db_data = session.query(NetTycJobMain).filter(
            NetTycJobMain.j_uuid == self.j_uuid).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.j_def_datetime=self.j_def_datetime
            db_data.j_start_datetime=self.j_start_datetime
            db_data.j_end_datetime=self.j_end_datetime
            db_data.j_status=self.j_status
            db_data.j_memo=self.j_memo


            


    @staticmethod
    def delete_all(db_session):
        db_session.query(NetTycJobMain).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.j_uuid

    def to_json(self):
        json_string = {
            'j_uuid': self.j_uuid,
            'j_status': self.j_status,
            'j_memo':self.j_memo,
            'j_def_datetime':json.dumps(self.j_def_datetime, cls=DateTimeEncoder),
            'j_start_datetime':json.dumps(self.j_start_datetime, cls=DateTimeEncoder),
            'j_end_datetime':json.dumps(self.j_end_datetime, cls=DateTimeEncoder),

            
            
            

        }
        return json_string