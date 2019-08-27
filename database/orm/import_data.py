
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


# 当前等待导入的数据
class ImportData(Base):
    __tablename__ = "import_data"
    u_uuid = Column(String(37), primary_key=True)
    u_create_datetime = Column(DateTime)
    u_queue_uuid = Column(String(37))
    u_start_download_datetime = Column(DateTime)
    u_end_download_datetime = Column(DateTime)
    u_start_import_datetime = Column(DateTime)
    u_end_import_datetime = Column(DateTime)
    u_node_edge = Column(String(64))
    u_label_items = Column(Text)
    u_edge_type = Column(Text)
    u_column_items = Column(Text)
    u_status = Column(String(64))  # 创建任务，开始下载，下载完成，开始导入，导入完成，已删除
    u_rowcount=Column(Integer)

    @staticmethod
    def saveOfUpdate(self, session):
        db_data = session.query(SystemCode).filter(
            SystemCode.code_main == self.code_main, SystemCode.code_code == self.code_code).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.code_desc = self.code_desc
            db_data.code_value = self.code_value
            db_data.f_trade = self.f_trade
            db_data.code_type = self.code_type

    @staticmethod
    def delete_all(db_session):
        db_session.query(ImportData).delete()

    def __repr__(self):
        return self.u_uuid+self.u_declare_key+self.u_body

    def to_json(self):
        json_string = {
            'u_uuid': self.u_uuid,
            'u_create_datetime': json.dumps(self.u_create_datetime, cls=DateTimeEncoder),
            'u_queue_uuid': self.u_queue_uuid,
            'u_start_download_datetime': json.dumps(self.u_start_download_datetime, cls=DateTimeEncoder),
            'u_end_download_datetime': json.dumps(self.u_end_download_datetime, cls=DateTimeEncoder),
            'u_start_import_datetime': json.dumps(self.u_start_import_datetime, cls=DateTimeEncoder),
            'u_end_import_datetime': json.dumps(self.u_end_import_datetime, cls=DateTimeEncoder),
            'u_node_edge': self.u_node_edge,
            'u_label_items': self.u_label_items,
            'u_edge_type': self.u_edge_type,
            'u_column_items': self.u_column_items,
            'u_status': self.u_status,
            'u_rowcount':self.u_rowcount,




        }
        return json_string