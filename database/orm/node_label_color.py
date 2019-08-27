import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric



class NodeLabelColor(Base):
    __tablename__ = "node_label_color"
    n_lable_classs = Column(String(256), primary_key=True)
    n_color = Column(String(6))
    n_lable_display = Column(String(256), unique=True)

    def to_json(self):
        json_string = {
            'n_lable_classs': self.n_lable_classs,
            'n_color': self.n_color,
            'n_display': self.n_display,


        }
        return json_string

    @staticmethod
    def delete_all(db_session):
        db_session.query(NodeLabelColor).delete()

    def saveOfUpdate(self, session):
        db_data = session.query(NodeLabelColor).filter(
            NodeLabelColor.n_lable_classs == self.n_lable_classs).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.n_color = self.n_color
            db_data.n_display = self.n_display