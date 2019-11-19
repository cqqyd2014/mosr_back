
#encoding=utf-8
import os
from database import get_db,ProcessDetail,QueryTemplate,JobQueue,ImportData
import datetime
from python_common.neo4j_common import command
import time


def neo4j_command():
        db_session=get_db()
        queue=db_session.query(JobQueue).filter(JobQueue.u_status=='发布',JobQueue.u_declare_key=='neo4j_command',JobQueue.u_publisher_id=='neo4j_command').order_by(JobQueue.u_publish_datetime.desc()).first()
        job=queue
        if (queue!=None):
                current=datetime.datetime.now()
                queue.u_start_datetime=current
                db_session.commit()
                body=queue.u_body
                print(body)
                command(body,None)
                current=datetime.datetime.now()
                queue.u_complete_datetime=current
                queue.u_status='处理完成'
                db_session.commit()
        db_session.close()
        #print("ok")