
import uuid
import datetime
import psutil
import platform

from database.orm_session import create_session
from database.orm import SystemPar,SystemCode,ProcessDetail,QueryTemplate,Neo4jCatalog,JobQueue,ImportData,CurrentNodeLabels,CurrentEdgeTypes,CurrentProperties


def run(socketio,l_type,long_process_command):
        #发送任务到queue
        
        db_session=create_session()
        import_neo4j_install_dir_db=db_session.query(SystemPar).filter(SystemPar.par_code=='import_neo4j_install_dir').one()
        start_time=datetime.datetime.now()
        import_neo4j_install_dir_value=import_neo4j_install_dir_db.par_value
        _queue_uuid=str(uuid.uuid1())
        _queue=JobQueue(u_uuid=_queue_uuid,u_declare_key=l_type,u_body=long_process_command,u_publisher_id=l_type,u_publish_datetime=start_time,u_no_ack=False,u_start_datetime=None,u_complete_datetime=None,u_status='发布')
        db_session.add(_queue)
        db_session.flush()
        db_session.commit()
        db_session.close()

        #循环检测状态看是否导入成功
        u_complete_datetime=None
        u_back_message=''
        while u_complete_datetime==None:
            socketio.sleep(10)
            mem=psutil.virtual_memory()
            disk=psutil.disk_usage(import_neo4j_install_dir_value)
            
            socketio.emit('system_report',{'platform':platform.platform(),'disk_total':disk.total,'disk_free':disk.free,'cpu_percent':psutil.cpu_percent(),'mem_total':mem.total,'mem_used':mem.used,'mem_free':mem.free}, broadcast=True)
            db_session_check=create_session()
            _queue_reload=db_session_check.query(JobQueue).filter(JobQueue.u_uuid==_queue_uuid).one()
            u_complete_datetime=_queue_reload.u_complete_datetime
            u_status=_queue_reload.u_status
            u_back_message=_queue_reload.u_back_message
            db_session_check.close()
        
        return u_back_message