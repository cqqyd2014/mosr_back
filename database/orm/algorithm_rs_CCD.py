
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


class AlgorithmRsCCD(Base):
    __tablename__ = "algorithm_rs_connected_components_d"
    u_uuid = Column(String(37), primary_key=True)
    u_setId	 = Column(Integer, primary_key=True)
    u_size=Column(Integer)
    
    

    @staticmethod
    def saveOfUpdate(self, session):
        db_data = session.query(AlgorithmRsCCD).filter(
            AlgorithmRsCCD.u_uuid == self.u_uuid,AlgorithmRsCCD.u_setId==self.u_setId).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            pass
           
            

    @staticmethod
    def delete_all(db_session):
        db_session.query(AlgorithmRsCCD).delete()

    def __repr__(self):
        return self.u_uuid

    def to_json(self):
        json_string = {
            'u_uuid': self.u_uuid,
            'u_size':self.u_size,
            'u_setId': self.u_setId,
            




        }
        return json_string