from mosr_back_orm.orm import create_session,SystemPar,init_db,SystemCode,ProcessDetail,SystemData,QueryTemplate,Neno4jCatalog,JobQueue,ImportData,CurrentNodeLabels,CurrentEdgeTyps,CurrentProperties
import uuid
import datetime
import psutil
import platform

def run(socketio,l_type,long_process_command):
        #发送任务到queue
        
        db_session=create_session()
        import_neo4j_install_dir=db_session.query(SystemPar).filter(SystemPar.par_code=='import_neo4j_install_dir').one()
        start_time=datetime.datetime.now()
        _queue_uuid=str(uuid.uuid1())
        _queue=JobQueue(u_uuid=_queue_uuid,u_declare_key=l_type,u_body=long_process_command,u_publisher_id=l_type,u_publish_datetime=start_time,u_no_ack=False,u_start_datetime=None,u_complete_datetime=None,u_status='发布')
        db_session.add(_queue)
        db_session.flush()
        db_session.commit()

        #循环检测状态看是否导入成功
        db_session_check=create_session()
        _queue=db_session_check.query(JobQueue).filter(JobQueue.u_uuid==_queue_uuid).one()
        u_complete_datetime=_queue.u_complete_datetime
        db_session_check.close()
        while u_complete_datetime==None:
            socketio.sleep(10)
            mem=psutil.virtual_memory()
            disk=psutil.disk_usage(import_neo4j_install_dir.par_value)
            
            socketio.emit('system_report',{'platform':platform.platform(),'disk_total':disk.total,'disk_free':disk.free,'cpu_percent':psutil.cpu_percent(),'mem_total':mem.total,'mem_used':mem.used,'mem_free':mem.free}, broadcast=True)
            db_session_check=create_session()
            _queue_reload=db_session_check.query(JobQueue).filter(JobQueue.u_uuid==_queue_uuid).one()
            u_complete_datetime=_queue_reload.u_complete_datetime
            u_status=_queue_reload.u_status
            db_session_check.close()
        db_session.close()