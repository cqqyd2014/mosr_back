
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


#每组的明细
class AlgorithmRsCCDD(Base):
    __tablename__ = "algorithm_rs_connected_components_dd"
    u_uuid = Column(String(37), primary_key=True)
    u_setId	 = Column(Integer, primary_key=True)
    u_nodeId = Column(Integer, primary_key=True)
    u_nodeName = Column(String(37))
    
    

    @staticmethod
    def saveOfUpdate(self, session):
        db_data = session.query(AlgorithmRsCCDD).filter(
            AlgorithmRsCCDD.u_uuid == self.u_uuid,AlgorithmRsCCDD.u_setId==self.u_setId,AlgorithmRsCCDD.u_nodeId==self.u_nodeId).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            pass
           
            

    @staticmethod
    def delete_all(db_session):
        db_session.query(AlgorithmRsCCDD).delete()

    def __repr__(self):
        return self.u_uuid

    def to_json(self):
        json_string = {
            'u_uuid': self.u_uuid,
            'u_nodeId':self.u_nodeId,
            'u_setId': self.u_setId,
            'u_nodeName':self.u_nodeName,
            




        }
        return json_string