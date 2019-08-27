import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


#Connected Components algorithm算法的结果

class AlgorithmRsCCM(Base):
    __tablename__ = "algorithm_rs_connected_components_m"
    u_uuid = Column(String(37), primary_key=True)
    u_create_datetime = Column(DateTime)
    u_queue_string = Column(String(1024))
    u_set_size=Column(Integer)
    

    @staticmethod
    def saveOfUpdate(self, session):
        db_data = session.query(AlgorithmRsCCM).filter(
            AlgorithmRsCCM.u_uuid == self.u_uuid).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.u_create_datetime = self.u_create_datetime
            db_data.u_queue_string = self.u_queue_string
            db_data.u_set_size=self.u_set_size
            

    @staticmethod
    def delete_all(db_session):
        db_session.query(AlgorithmRsCCM).delete()

    def __repr__(self):
        return self.u_uuid

    def to_json(self):
        json_string = {
            'u_uuid': self.u_uuid,
            'u_create_datetime': json.dumps(self.u_create_datetime, cls=DateTimeEncoder),
            'u_queue_string': self.u_queue_string,
            'u_set_size':self.u_set_size
            




        }
        return json_string