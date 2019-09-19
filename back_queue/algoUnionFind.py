
#encoding=utf-8
import os
from database import AlgorithmRsCCDD,AlgorithmRsCCD,AlgorithmRsCCM,get_db,SystemPar,SystemCode,ProcessDetail,QueryTemplate,JobQueue,ImportData
import datetime
from python_common.neo4j_common import command
import time
import uuid
import datetime
from .opendb_getjob import opendb_getjob



def readData(command_sql,records):
        db_session=create_session()
        uuid_str=str(uuid.uuid1())
        #print(uuid_str)
        
        setId=-1
        setSize=0#每个组的大小
        set_size=0#有多少个组

        for record in records:
                #print(record)
                
                
                #print(record['setId'])
                if setId!=record['setId']:
                        #新的setId
                        if setId!=-1:
                                
                                algorithmRsCCD=AlgorithmRsCCD(u_uuid=uuid_str,u_setId=setId,u_size=setSize)
                                db_session.add(algorithmRsCCD)
                        setId=record['setId']
                        setSize=0
                        set_size+=1
               
                algorithmRsCCDD=AlgorithmRsCCDD(u_uuid=uuid_str,u_setId=setId,u_nodeId=record['nodeId'],u_nodeName=record['node_name'])
                db_session.add(algorithmRsCCDD)
                setSize+=1

        algorithmRsCCD=AlgorithmRsCCD(u_uuid=uuid_str,u_setId=setId,u_size=setSize)
        db_session.add(algorithmRsCCD)


        algorithmRsCCM=AlgorithmRsCCM(u_uuid=uuid_str,u_create_datetime=datetime.datetime.now(),u_queue_string=command_sql,u_set_size=set_size+1)
        db_session.add(algorithmRsCCM)

        db_session.commit()
        db_session.close()
        return uuid_str


def unionFind():
        opendb_getjob('algo.unionFind',job)
    
def job(db_session,queue,current):
       
        body=queue.u_body
        print(body)
        rs_uuid=command(body,readData)
        command('match ()-[r:KNOWS]-() delete r',None)
        current=datetime.datetime.now()
        
        queue.u_back_message=rs_uuid
        db_session.commit()
        return current
        