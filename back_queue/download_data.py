import os
from neo4j import GraphDatabase
from database import get_db,ProcessDetail,QueryTemplate,JobQueue,ImportData
import datetime
import uuid
from sqlalchemy import desc
import json
import ast
import csv
import sys
from .opendb_getjob import opendb_getjob
from system.database.orm import *



from python_common.database_common import Database



def make_headers(column_items,body_dict):
    headers=[]
    if (body_dict['node_edge']=='node'):
        #节点的文件头
        for item in column_items:
            if item[2]=='编码':
                headers.append(item[0]+":ID")
            elif item[2]=='显示名称':
                headers.append("显示名称:"+item[1])
            elif item[2]=='不导入':
                pass
                
            else:
                headers.append(item[0]+":"+item[1])
    else:
        #关系的文件头
        for item in column_items:
            if item[2]=='起点':
                headers.append(":START_ID")
            elif item[2]=='终点':
                headers.append(":END_ID")
            elif item[2]=='不导入':
                pass
            else:
                headers.append(item[0]+":"+item[1])
    return headers

def job(db_session,queue,current):

    #对应的import_data不是删除状态
    importData=db_session.query(ImportData).filter(ImportData.u_queue_uuid==queue.u_uuid).one()
    if (importData.u_status=='已删除'):
        pass
    else:
        #有待处理记录
        importData.u_start_download_datetime=current
        importData.u_status='开始下载'
        db_session.commit()
        #解析body中的数据
        body=queue.u_body
        body_dict = ast.literal_eval(body)
                #print(body_dict)
                #重建column_items
        column_items=[]
        db_column_items=body_dict['column_items'].split(',')
                #print(len(db_column_items))
        flag=0
        while flag<len(db_column_items):
            new_item=[]
                    #print(flag)
                    #print(db_column_items[flag])
            new_item.append(db_column_items[flag])
            flag+=1
            new_item.append(db_column_items[flag])
            flag+=1
            new_item.append(db_column_items[flag])
            column_items.append(new_item)
            flag+=1
                #print(column_items)
        database=Database(body_dict['db_type'],body_dict['db_address'],body_dict['db_port'],body_dict['db_name'],body_dict['db_username'],body_dict['db_password'])
        database.getConnection()
                #读取批量处理的批次数
        db_download_batch=db_session.query(SystemPar).filter(SystemPar.par_code=='download_batch').one()
        db_csv_batch=db_session.query(SystemPar).filter(SystemPar.par_code=='csv_batch').one()
        db_import_neo4j_install_dir=db_session.query(SystemPar).filter(SystemPar.par_code=='import_neo4j_install_dir').one()
        download_batch=int(db_download_batch.par_value)
        csv_batch=int(db_csv_batch.par_value)
        import_neo4j_install_dir=db_import_neo4j_install_dir.par_value
        select_table=body_dict['select_table']
        database.openBatchCursor(select_table,column_items)
        database.getBatchCursorRowCount()
        rows=database.getBatchCursorRows(download_batch)
                #print("csv start")
                #生成csv文件
        if not os.path.exists(import_neo4j_install_dir+"import/"):
            os.mkdir(import_neo4j_install_dir+"import/")
        if os.path.exists(import_neo4j_install_dir+"import/"+queue.u_uuid):
            os.remove(import_neo4j_install_dir+"import/"+queue.u_uuid)
                #print("start")
        with open(import_neo4j_install_dir+"import/"+queue.u_uuid,'w', encoding='utf-8',newline='')as f:
            f_csv = csv.writer(f,quoting=csv.QUOTE_ALL)
            f_csv.writerow(make_headers(column_items,body_dict))
            while (rows!=[]):
                f_csv.writerows(rows)
                        #print(rows)
                rows=database.getBatchCursorRows(download_batch)
        importData.u_rowcount=database.getBatchCursorRowCount()
        database.closeBatchCursor()
        database.closeConnection()
        current=datetime.datetime.now()
        importData.u_end_download_datetime=current
    db_session.commit()
    return current



def download_data():
    opendb_getjob('download_data',job)
        
    

def main():

    download_data()

if __name__ == '__main__':
  main()