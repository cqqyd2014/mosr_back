from database import get_db,ProcessDetail,QueryTemplate,JobQueue,ImportData
import datetime
import sys


from system.database.orm import *

def opendb_getjob(u_declare_key,job):
   
    try:
        db_session=get_db()

        queue=db_session.query(JobQueue).filter(JobQueue.u_status=='发布',JobQueue.u_declare_key==u_declare_key,JobQueue.u_publisher_id==u_declare_key).order_by(JobQueue.u_publish_datetime.desc()).first()

        
        if (queue!=None):
            current=datetime.datetime.now()
            queue.u_start_datetime=current
            queue.u_status='处理中'
            db_session.commit()
            current=job(db_session,queue,current)
            current=datetime.datetime.now()
            queue.u_complete_datetime=current
            queue.u_status='处理完成'
            db_session.commit()
    except Exception as ex:
        db_session.rollback()
        print(ex)

    finally:
        db_session.close()