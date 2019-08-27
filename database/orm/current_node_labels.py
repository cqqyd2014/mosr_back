
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric



#当前系统中的节点标签
class CurrentNodeLabels(Base):
    __tablename__ = "current_node_labels"
    labels = Column(String(1024), primary_key=True)
    label = Column(String(1024), primary_key=True)
    create_datetime=Column(DateTime)
    

    @staticmethod
    def saveOrUpdate(self, session):
        db_data = session.query(CurrentNodeLabels).filter(
            CurrentNodeLabels.labels == self.labels, CurrentNodeLabels.label == self.label).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            pass

    @staticmethod
    def delete_all(db_session):
        db_session.query(CurrentNodeLabels).delete()
        #print("删除成功")


    def __repr__(self):
        return self.labels+self.label

    def to_json(self):
        json_string = {
            'labels': self.labels,
            'label': self.label,
            'create_datetime': json.dumps(self.create_datetime, cls=DateTimeEncoder),
            

        }
        return json_string