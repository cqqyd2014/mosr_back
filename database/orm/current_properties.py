

import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


#当前系统中的属性
class CurrentProperties(Base):
    __tablename__ = "current_properties"
    u_uuid=Column(String(37), primary_key=True)
    u_type = Column(String(32))
    u_label_type=Column(String(512))
    u_column_name=Column(String(512))
    u_column_type=Column(String(512))
    create_datetime=Column(DateTime)
    
    

    @staticmethod
    def saveOfUpdate(self, session):
        db_data = session.query(CurrentProperties).filter(
            CurrentProperties.u_uuid == self.u_uuid).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            pass

    @staticmethod
    def delete_all(db_session):
        db_session.query(CurrentProperties).delete()


    def __repr__(self):
        return self.u_uuid
    
    def to_json(self):
        json_string = {
            'u_uuid': self.u_uuid,
            'u_type': self.u_type,
            'u_label_type': self.u_label_type,
            'u_column_name': self.u_column_name,
            'u_column_type': self.u_column_type,
            'create_datetime': json.dumps(self.create_datetime, cls=DateTimeEncoder),
            

        }
        return json_string