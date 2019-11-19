from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Numeric,Column, Integer, String, ForeignKey, DateTime, Numeric, Float, Text, Date, Boolean
Base = declarative_base()





from .algorithm_rs_CCD import AlgorithmRsCCD
from .algorithm_rs_CCDD import AlgorithmRsCCDD
from .algorithm_rs_CCM import AlgorithmRsCCM
from .current_edge_types import CurrentEdgeTypes
from .current_node_labels import CurrentNodeLabels
from .current_properties import CurrentProperties
from .import_data import ImportData
from .job_queue import JobQueue
from .neo4j_catalog import Neo4jCatalog
from .node_label_color import NodeLabelColor
from .process_detail import ProcessDetail
from .query_template import QueryTemplate


postgresql_conn_str = "postgresql+psycopg2://xywl2019:Wang1980@postgres11:33133/xywl2019"
engine = create_engine(postgresql_conn_str, isolation_level = 'READ COMMITTED',pool_size=10)