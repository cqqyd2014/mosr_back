import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


#当前系统中的关系类型
class CurrentEdgeTypes(Base):
    __tablename__ = "current_edge_types"
    edge_type = Column(String(1024), primary_key=True)
    create_datetime=Column(DateTime)


    
    

    @staticmethod
    def saveOrUpdate(self, session):
        db_data = session.query(CurrentEdgeTyps).filter(
            CurrentEdgeTyps.edge_type == self.edge_type).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            pass

    @staticmethod
    def delete_all(db_session):
        db_session.query(CurrentEdgeTyps).delete()

        


    def __repr__(self):
        return self.edge_type

    def to_json(self):
        json_string = {
            'edge_type': self.edge_type,
            'create_datetime': json.dumps(self.create_datetime, cls=DateTimeEncoder),
            

        }
        return json_string