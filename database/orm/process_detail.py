import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric,ForeignKey



class ProcessDetail(Base):
    __tablename__ = "process_detail"
    pd_uuid = Column(String(37), primary_key=True)
    pd_start_datetime = Column(DateTime)
    pd_catalog = Column(String(32), ForeignKey('system_code.code_code'))
    pd_command = Column(Text)

    def to_json(self):

        json_string = {
            'pd_uuid': self.pd_uuid,
            'pd_start_datetime': json.dumps(self.pd_start_datetime, cls=DateTimeEncoder),
            'pd_catalog': self.pd_catalog,
            'pd_command': self.pd_command,

        }

        return json_string

    @staticmethod
    def delete_all(db_session):
        db_session.query(ProcessDetail).delete()

    def saveOfUpdate(self, session):
        db_data = session.query(ProcessDetail).filter(
            ProcessDetail.pd_uuid == self.pd_uuid).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.pd_start_datetime = self.pd_start_datetime
            db_data.pd_catalog = self.pd_catalog
            db_data.pd_command = self.pd_command


def _create_db_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def create_session():

    Session = sessionmaker(bind=engine)
    session = Session()

    return session