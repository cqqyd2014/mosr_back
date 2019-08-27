


import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


class QueryTemplate(Base):
    __tablename__ = "query_template"
    qt_uuid = Column(String(37), primary_key=True)
    qt_datetime = Column(DateTime)
    qt_object = Column(Text)
    qt_cypher = Column(Text)
    qt_title = Column(String(1024))
    qt_desc = Column(Text)
    qt_type = Column(String(64))

    def to_json(self):

        json_string = {
            'qt_uuid': self.qt_uuid,
            'qt_datetime': json.dumps(self.qt_datetime, cls=DateTimeEncoder),
            'qt_object': self.qt_object,
            'qt_cypher': self.qt_cypher,
            'qt_title': self.qt_title,
            'qt_desc': self.qt_desc,
            'qt_type': self.qt_type

        }

        return json_string