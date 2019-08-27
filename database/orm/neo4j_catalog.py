
import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric


class Neo4jCatalog(Base):
    __tablename__ = "neo4j_catlog"
    nc_uuid = Column(String(37), primary_key=True)
    nc_update_datetime = Column(DateTime)
    nc_type = Column(String(64))
    nc_value = Column(String(512))

    def to_json(self):

        json_string = {
            'nc_uuid': self.nc_uuid,
            'nc_update_datetime': json.dumps(self.nc_update_datetime, cls=DateTimeEncoder),
            'nc_type': self.nc_type,
            'nc_value': self.nc_value,


        }

        return json_string