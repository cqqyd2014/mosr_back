from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,jsonify,current_app
import json
from long_time_process import run as long_run
from flask_cors import CORS
from mosr_back_orm.orm import create_session,SystemPar,init_db,SystemCode,ProcessDetail,SystemData,QueryTemplate,Neno4jCatalog,JobQueue,ImportData,CurrentNodeLabels,CurrentEdgeTyps,CurrentProperties
from restful import TableRestful
import os
from neo4j import GraphDatabase
from python_common.neo4j_common import buildNodes,buildEdges,createNode,getPath,getJson,createEdge
import datetime
import uuid
from python_common.common import Base64Uri
import decimal
import urllib
import platform
import subprocess
import _thread
from flask.json import JSONEncoder as _JSONEncoder
import time
from eventlet.green import threading
import psutil

class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):  # for decimal
            return float(obj)
        elif isinstance(obj, datetime.datetime):  # for datetime
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, obj)



import sys
sys.path.append("python_common")
sys.path.append("mosr_back_orm")
from python_common.database_common import Database
from flask_socketio import SocketIO,emit

app=Flask(__name__)
app.config['SECRET_KEY'] = 'S'
app.json_encoder = JSONEncoder
CORS(app, resources=r'/*')
socketio = SocketIO(app)
from threading import Lock
thread = None
thread_lock = Lock()

#socketio.init_app(app)
#name_space ='/neo4j_rebuild'
'''
temp_dir="d:/temp/"

system_default_dir="D:/software/neo4j-community-3.5.3/"

@app.route('/systemstatus/')
def system_status():
    import win32file
    res_list = win32file.GetDiskFreeSpace(system_default_dir)
    disk_free_space = res_list[0]*res_list[1]*res_list[2]/(1024*1024.0)
    return jsonify({'free_space':disk_free_space,'system_default_dir':system_default_dir})
'''

#去除空格和逗号
def _blankAndoComma(_str):
    _str=_str.replace(' ','')
    _str=_str.replace(',','_')
    return _str



@app.route('/')
def show_entries():
    user_agent=request.headers.get('User_Agent')
    return 'user_agent is %s' %user_agent


@app.route('/neo4jsampledata/')
def neo4j_sample_data():
    driver=GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Wang1980"))
    with driver.session() as session:
        result = session.run("match p=((n)-[]-()) return p limit 50")
        graph=result.graph()
        nodes=graph.nodes
        nodes_object=[]
        for node in nodes:
            node_object=buildNodes(node)
            nodes_object.append(node_object)
        relationships_object=[]
        relationships=graph.relationships
        for r in relationships:
            r_object=buildEdges(r)
            relationships_object.append(r_object)
        
        session.close()
        return jsonify(elements = {"nodes": nodes_object, "edges": relationships_object})


def convertToTitle(n):
        """
        :type n: int
        :rtype: str
        """
        rStr = ""
        while n!=0:
            res = n%26
            if res == 0:
                res =26
                n -= 26
            rStr = chr(ord('A')+res-1) + rStr
            n = n//26
        return rStr



   # queue中保存的数据应该为导入任务，包括sql的信息、字段信息以及将要生成的数据文件名

    #另外，还有一个现有数据列表




@app.route('/import_queue_upload/',methods=['POST'])
def import_queue_upload():

    
    db_type=request.form.get('db_type')
    db_address=request.form.get('db_address')
    db_port=request.form.get('db_port')
    db_name=request.form.get('db_name')
    db_username=request.form.get('db_username')
    db_password=request.form.get('db_password')
    select_table=request.form.get('select_table')
    column_items=request.form.get('column_items')
    label_items=request.form.get('label_items')
    node_edge=request.form.get('node_edge')
    edge_type=request.form.get('edge_type')
    #从数据库得到neo4j的安装路径
    db_session=create_session()
    import_neo4j_install_dir=db_session.query(SystemPar).filter(SystemPar.par_code=='import_neo4j_install_dir').one()
    db_session.close()

    #queue_uuid是queue的id，也是文件名

    create_pub_time=datetime.datetime.now()
    queue_uuid=str(uuid.uuid1())


    u_body={'db_type':db_type,'db_address':db_address,'db_port':db_port,'db_name':db_name,'db_username':db_username,'db_password':db_password,'select_table':select_table,'column_items':column_items,'label_items':label_items,'node_edge':node_edge,'edge_type':edge_type}
    print(edge_type)
    queue=JobQueue(u_uuid=queue_uuid,u_declare_key='download_data',u_body=str(u_body),u_publisher_id='import_queue_upload',u_publish_datetime=create_pub_time,u_no_ack=False,u_start_datetime=None,u_complete_datetime=None,u_status='发布')
    db_session=create_session()
    db_session.add(queue)
    db_session.commit()
    db_session.close()
    #数据导入列表
    import_uuid=str(uuid.uuid1())
    import_data=ImportData(u_uuid=import_uuid,u_create_datetime=create_pub_time,u_queue_uuid=queue_uuid,u_start_download_datetime=None,u_end_download_datetime=None,u_start_import_datetime=None,u_end_import_datetime=None,u_node_edge=node_edge,u_label_items=label_items,u_edge_type=edge_type,u_column_items=column_items,u_status='创建任务')
    db_session=create_session()
    db_session.add(import_data)
    db_session.commit()
    db_session.close()

    
    return jsonify({'status':'success'})



'''
@app.route('/nodes_upload/',methods=['POST'])
def nodes_upload():
    f = request.files['file']
    basepath = os.path.dirname(temp_dir)#当前文件所在路径
    upload_path = os.path.join(basepath,str(uuid.uuid1()))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)
    f.close()

    #处理标签
    label_items=json.loads(request.form.get('label_items'))
    node_type=request.form.get('node_type')
    app = xw.App(visible=False, add_book=False)
    wb = xw.Book(upload_path)
    sht = wb.sheets[0]
    #data=sht.range('A1').value
    column_items=request.form.get('column_items')
    items_jsons=json.loads(column_items)
    row_flag=2#从第二行开始导入
    driver=GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Wang1980"))
    
    with driver.session() as session:
        while sht.range('A'+str(row_flag)).value!=None:
            #处理一行数据
            col_flag=1
            row_data={}
            for item in items_jsons:
                #print(str(convertToTitle(col_flag))+str(row_flag))
                col_value=sht.range(str(convertToTitle(col_flag))+str(row_flag)).value
                #print(col_value)
                if item['type']!='不导入':
                    if item['type']=='其他属性':
                        column=item['column']
                        #print(column)
                        row_data[column]=col_value
                    if item['type']=='编码':
                        row_data['ID']=col_value
                    if item['type']=='显示名称':
                        row_data['name']=col_value
                col_flag+=1
            #print(row_data)
            #print(label_items)
            create_string=createNode(row_data,node_type,label_items)
            session.run(create_string)
            
            row_flag+=1
        session.close()
    wb.close()
    app.quit()
    
    return jsonify({'status':'success'})


@app.route('/edges_upload/',methods=['POST'])
def edges_upload():
    f = request.files['file']
    basepath = os.path.dirname(temp_dir)#当前文件所在路径
    upload_path = os.path.join(basepath,str(uuid.uuid1()))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)
    f.close()

    #处理标签
    edge_type=request.form.get('edge_type')
    app = xw.App(visible=False, add_book=False)
    wb = xw.Book(upload_path)
    sht = wb.sheets[0]
    #data=sht.range('A1').value
    column_items=request.form.get('column_items')
    items_jsons=json.loads(column_items)
    row_flag=2#从第二行开始导入
    driver=GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Wang1980"))
    
    with driver.session() as session:
        while sht.range('A'+str(row_flag)).value!=None:
            #处理一行数据
            col_flag=1
            row_data={}
            for item in items_jsons:
                #print(str(convertToTitle(col_flag))+str(row_flag))
                col_value=sht.range(str(convertToTitle(col_flag))+str(row_flag)).value
                #print(col_value)
                if item['type']!='不导入':
                    if item['type']=='其他属性':
                        column=item['column']
                        #print(column)
                        row_data[column]=col_value
                    if item['type']=='起点':
                        row_data['START']=col_value
                    if item['type']=='终点':
                        row_data['END']=col_value
                col_flag+=1
            #print(row_data)
            #print(label_items)
            create_string=createEdge(row_data,edge_type)
            session.run(create_string)
            
            row_flag+=1
        session.close()
    wb.close()
    app.quit()
    
    return jsonify({'status':'success'})
'''
@app.route('/neo4jdata/')
def neo4j_data():
    if  'neo4jgraph_cypher' in request.args:

        db_session=create_session()
        systemCodes=db_session.query(SystemCode).filter(SystemCode.code_main=='node_color').all()
        colors=[]
        for sc in systemCodes:
            colors.append(sc.code_code)
        db_session.close()
        return getPath(Base64Uri.decode(request.args['neo4jgraph_cypher']),colors)
        
    else:
        pass

@app.route('/test_connection/',methods=['POST'])
def test_connection():
    
    request.get_json(silent=True)
    db_type=request.json['db_type']
    db_address=request.json['db_address']
    db_port=request.json['db_port']
    db_name=request.json['db_name']
    db_username=request.json['db_username']
    db_password=request.json['db_password']
    database=Database(db_type,db_address,db_port,db_name,db_username,db_password)
    #print(database.db_type)
    return jsonify(database.testConnection())

@app.route('/get_tables/',methods=['POST'])
def get_tables():
    
    request.get_json(silent=True)
    db_type=request.json['db_type']
    db_address=request.json['db_address']
    db_port=request.json['db_port']
    db_name=request.json['db_name']
    db_username=request.json['db_username']
    db_password=request.json['db_password']
    database=Database(db_type,db_address,db_port,db_name,db_username,db_password)
    database.getConnection()
    tables=database.getTables()
    database.closeConnection()
    return jsonify(tables)
        
  
@app.route('/get_cols/',methods=['POST'])
def get_cols():
    
    request.get_json(silent=True)
    db_type=request.json['db_type']
    db_address=request.json['db_address']
    db_port=request.json['db_port']
    db_name=request.json['db_name']
    db_username=request.json['db_username']
    db_password=request.json['db_password']
    select_table=request.json['select_table']
    database=Database(db_type,db_address,db_port,db_name,db_username,db_password)
    database.getConnection()
    cols=[]
    try:
        cols=database.getColumn(select_table)
        #print("ok")
        #print(cols)
    except:
        cols=[]
    finally:
        pass
    #print(jsonify(cols))
    database.closeConnection()
    return jsonify(cols)

@app.route('/get_top_row_cells/',methods=['POST'])
def get_top_row_cells():
    
    request.get_json(silent=True)
    db_type=request.json['db_type']
    db_address=request.json['db_address']
    db_port=request.json['db_port']
    db_name=request.json['db_name']
    db_username=request.json['db_username']
    db_password=request.json['db_password']
    select_table=request.json['select_table']
    top=request.json['top']
    database=Database(db_type,db_address,db_port,db_name,db_username,db_password)
    database.getConnection()
    cols=database.getColumn(select_table)
    #print(cols)
    cells=database.getTopRowCells(select_table,top,cols)
    #print("cols")
    #print(jsonify(cols))
    database.closeConnection()
    return jsonify(cells)



@app.route('/import_data/')
def import_data():
    #print("import_get...............................")
    empty=[]
    if not request.args:
        db_session=create_session()
        posts=db_session.query(ImportData).filter(ImportData.u_status!='已删除').all()
        #print("import中国")
        for post in posts:
            empty.append(post.to_json())
        db_session.close()
        return jsonify(empty)
    else:
        db_session=create_session()
        posts=db_session.query(ImportData).filter(ImportData.u_status!='已删除').all()
        for post in posts:
            empty.append(post.to_json())
        db_session.close()
        return  jsonify(empty)


@app.route('/import_data/<uuid>', methods=['PUT'])
def update_import_data(uuid):
    if len(uuid) == 0:
        abort(404)
    if not request.json:
        abort(400)
    request.get_json(silent=True)
    u_status=request.json['u_status']
    db_session=create_session()
    
    import_data=db_session.query(ImportData).filter(ImportData.u_uuid==uuid).one()
    import_data.u_status=u_status
    #删除文件
    db_import_neo4j_install_dir=db_session.query(SystemPar).filter(SystemPar.par_code=='import_neo4j_install_dir').one()
    import_neo4j_install_dir=db_import_neo4j_install_dir.par_value
    file_path=import_neo4j_install_dir+"import/"+import_data.u_queue_uuid
    #print(file_path)
    #print(os.path.exists(file_path))
    if os.path.exists(file_path):
        print("start reomve")
        os.remove(file_path)
    db_session.commit()
    db_session.close()
    
    return jsonify({'result': True})



@app.route('/import_data/<uuid>', methods=['DELETE'])
def delete_import_data(uuid):
    
    if len(uuid) == 0:
        abort(404)
    db_session=create_session()
    
    post=db_session.query(ImportData).filter(ImportData.u_uuid==uuid).delete()
    db_session.commit()
    db_session.close()
    return jsonify({'result': True})



@app.route('/my_templates/<uuid>', methods=['DELETE'])
def delete_my_templates(uuid):
    
    if len(uuid) == 0:
        abort(404)
    db_session=create_session()
    
    post=db_session.query(QueryTemplate).filter(QueryTemplate.qt_uuid==uuid).delete()
    db_session.commit()
    db_session.close()
    return jsonify({'result': True})

@app.route('/my_templates/')
def my_templates():
    empty=[]
    if not request.args:
        db_session=create_session()
        posts=db_session.query(QueryTemplate).all()
        for post in posts:
            empty.append(post.to_json())
        db_session.close()
        return jsonify(empty)
    else:
        db_session=create_session()
        posts=db_session.query(QueryTemplate).filter(QueryTemplate.qt_type==request.args['qt_type']).all()
        for post in posts:
            empty.append(post.to_json())
        db_session.close()
        return  jsonify(empty)


    
    
        
    



@app.route('/SystemPar/',methods=['POST'])
def new_system_par():

    systemPar=SystemPar.from_json(request.json)
    db_session=create_session()
    db_session.add(systemPar)
    db_session.close()

@app.route('/SystemPar/',methods=['GET'])
def get_posts():
    empty=[]
    if not request.args:
        db_session=create_session()
        posts=db_session.query(SystemPar).all()
        for post in posts:
            empty.append(post.to_json())
        db_session.close()
        return jsonify(empty)
    else:
        db_session=create_session()
        post=db_session.query(SystemPar).filter(SystemPar.par_code==request.args['par_code']).one()
        db_session.close()
        return  jsonify(post.to_json())
'''     
@app.route('/NodeColors/',methods=['GET'])
def node_colors():
    empty=[]
    if not request.args:
        db_session=create_session()
        posts=db_session.query(NodeColor).all()
        for post in posts:
            empty.append(post.to_json())
        db_session.close()
        return jsonify(empty)
    else:
        db_session=create_session()
        post=db_session.query(NodeColor).filter(NodeColor.n_lable==request.args['n_lable']).all()
        db_session.close()
        return  jsonify(post.to_json())
'''


@app.route('/neo4j_catlog_properties_code/',methods=['GET'])
def neo4j_catlog_properties_code():
    empty=None
    db_session=create_session()
    #print(request.args['u_label_type'])
    post=db_session.query(CurrentProperties).filter(CurrentProperties.u_label_type=='[\''+request.args['u_label_type']+'\']',CurrentProperties.u_column_type=='编码').one()
    empty={'u_column_name':post.u_column_name}
    #print(post.u_column_name)
    db_session.close()
    return  jsonify(empty)

@app.route('/neo4j_catlog_properties/',methods=['GET'])
def neo4j_catlog_properties():
    empty=[]
    db_session=create_session()
    posts=db_session.query(CurrentProperties.u_type,CurrentProperties.u_column_name,CurrentProperties.u_column_type).group_by(CurrentProperties.u_type,CurrentProperties.u_column_name,CurrentProperties.u_column_type).all()
    for post in posts:
        empty.append({'u_type':post.u_type,'u_column_name':post.u_column_name,'u_column_type':post.u_column_type})
    db_session.close()
    return  jsonify(empty)

@app.route('/neo4j_catlog_edgetypes/',methods=['GET'])
def neo4j_catlog_edgetypes():
    empty=[]
    db_session=create_session()
    posts=db_session.query(CurrentEdgeTyps).all()
    for post in posts:
        empty.append(post.to_json())
    db_session.close()
    return  jsonify(empty)

@app.route('/neo4j_catlog_nodelabels/',methods=['GET'])
def neo4j_catlog_nodelabels():
    empty=[]
    db_session=create_session()
    posts=db_session.query(CurrentNodeLabels).all()
    for post in posts:
        empty.append(post.to_json())
    db_session.close()
    return  jsonify(empty)


@app.route('/neo4j_catlog/',methods=['POST'])
def post_neo4j_catlog():
    request.get_json(silent=True)
    if not request.json :
        abort(400)
    neno4jCatalog=Neno4jCatalog(nc_uuid=str(uuid.uuid1()),nc_update_datetime=datetime.datetime.now(),nc_type=request.json['nc_type'],nc_value=request.json['nc_value'])
    db_session=create_session()
    db_session.add(neno4jCatalog)
    pd_json= neno4jCatalog.to_json()
    db_session.commit()
    db_session.close()
    return jsonify({'neo4j_catlog':pd_json}), 201



@app.route('/SystemCode/',methods=['GET'])
def get_systemcodes():
    empty = []
    if not request.args:
        # 没有指定id则返回全部
        db_session=create_session()
        posts=db_session.query(SystemCode).all()
        
        for post in posts:
            empty.append(post.to_json())
        db_session.close()
        return jsonify(empty)
        
    elif 'code_main' in request.args and 'code_code' not in request.args:
        db_session=create_session()
        posts=db_session.query(SystemCode).filter(SystemCode.code_main==request.args['code_main']).all()
        for post in posts:
            empty.append(post.to_json())
        db_session.close()
        return jsonify(empty)
    else:
        db_session=create_session()
        post=db_session.query(SystemCode).filter(SystemCode.code_main==request.args['code_main'],SystemCode.code_code==request.args['code_code']).one()
        db_session.close()
        return jsonify(post.to_json())

@app.route('/ProcessDetail/',methods=['POST'])
def post_process_detail():
    request.get_json(silent=True)
    if not request.json :
        abort(400)
    

    data=request.get_json()
    processDetail=ProcessDetail(pd_uuid=str(uuid.uuid1()),pd_start_datetime=datetime.datetime.now(),pd_catalog=data['pd_catalog'],pd_command=data['pd_command'])
    db_session=create_session()
    db_session.add(processDetail)
    pd_json= processDetail.to_json()
    db_session.commit()
    db_session.close()
    return jsonify({'ProcessDetail':pd_json}), 201



@app.route('/SaveTemplate/',methods=['POST'])
def save_template():
    request.get_json(silent=True)
    if not request.json :
        abort(400)
    qt_object=Base64Uri.decode(request.json['qt_object'])
    qt_cypher=Base64Uri.decode(request.json['qt_cypher'])
    queryTemplate=QueryTemplate(qt_uuid=str(uuid.uuid1()),qt_datetime=datetime.datetime.now(),qt_type=request.json['qt_type'],qt_object=qt_object,qt_cypher=qt_cypher,qt_title=request.json['qt_title'],qt_desc=request.json['qt_desc'])
    db_session=create_session()
    db_session.add(queryTemplate)
    pd_json= queryTemplate.to_json()
    db_session.commit()
    db_session.close()
    return jsonify({'queryTemplate':pd_json}), 201



@app.route('/ProcessDetail/',methods=['GET'])
def get_process_detail():
    empty = []
    class Process_detail(TableRestful):
        def __init__(self,args,db_session):
            super(Process_detail, self).__init__(args,db_session)
            self.query=self.db_session.query(ProcessDetail,SystemCode)

        def _query_parmeter(self):
            if 'start_datetime_begin' in self.args and 'start_datetime_end' in self.args:
                self.q_filter=self.q_join.filter(ProcessDetail.start_datetime >=request.args['start_datetime_begin'],ProcessDetail.start_datetime <=request.args['start_datetime_end'])
            else:
                self.q_filter=self.q_join
            self.q_filter=self.q_filter.filter(SystemCode.code_code==ProcessDetail.pd_catalog)
        
        def _ordery_by(self):
            self.q_order=self.q_filter.order_by(ProcessDetail.pd_start_datetime.desc())
        
        def _join(self):
            self.q_join=self.query
    db_session=create_session()
    pd=Process_detail(request.args,db_session)
    rs=pd.get_rs_all()

    #print(rs)
    for r,s in rs:
        empty.append({'process_detail':r.to_json(),'system_code':s.to_json()})
        #print(s)
    db_session.close()
    return jsonify(empty)

@app.route('/SystemData/',methods=['GET'])
def get_system_data():
    empty = []
    class System_data(TableRestful):
        def __init__(self,args,db_session):
            super(System_data, self).__init__(args,db_session)
            self.query=self.db_session.query(SystemData)

        def _query_parmeter(self):
            self.q_filter=self.q_join
            
        
        def _ordery_by(self):
            self.q_order=self.q_filter
        
        def _join(self):
            self.q_join=self.query
    db_session=create_session()
    pd=System_data(request.args,db_session)
    rs=pd.get_rs_all()

    for r in rs:
        empty.append({'system_data':r.to_json()})
        #print(s)
    db_session.close()
    return jsonify(empty)

@socketio.on('neo4j_algo')
def neo4j_algo(par):
    print(par)
    if par['type']=='algo.unionFind':
        #返回一个uuid
        uuid=long_run(socketio,'algo.unionFind',par['sql'])



@socketio.on('neo4j_commands')
def neo4j_commands(commands):
    #long_run(socketio,'import_data',import_command)
    for command in commands:
        print(command)
        _name=command['_name']
        _command=command['_command']
        long_run(socketio,'neo4j_command',_command)
        socketio.start_background_task(long_time_process,{'message_type':"neo4j_command", 'message_info':_name+'处理完成'})
    socketio.start_background_task(long_time_process,{'message_type':"command_end", 'message_info':''})




@socketio.on('neo4j_rebuild')
def neo4j_rebuild(manage_import_data,import_data):
    
    socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_start", 'message_info':'系统开始重建分析数据库，业务将暂时中止，需等待数据库重建完成'})
    
    
    #emit('neo4j_rebuild_start', {'message': '系统开始重建分析数据库，业务将暂时中止，需等待数据库重建完成'}, broadcast=True)
    #print(manage_import_data)
    #print(import_data)
    #print(len(manage_import_data))
    #如果两个列表的数量不一致，不能重建
    if len(manage_import_data)!=len(import_data):
        socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_end", 'messsage_info':'重建未成功'})
        #emit('neo4j_rebuild_end', {'message': '重建未成功'}, broadcast=True)
    else:
        system_type=''
        if platform.platform().find('Windows')>=0:
            system_type='Windows'
        else:
            system_type='UNIX'
        import_command=''
        db_session=create_session()
        import_neo4j_install_dir=db_session.query(SystemPar).filter(SystemPar.par_code=='import_neo4j_install_dir').one()
        import_command+=import_neo4j_install_dir.par_value+'bin/'+('neo4j-admin.bat' if system_type=='Windows' else 'neo4j-admin')+' import'
        #import_command+=' --mode csv --database graph.db '
        #print(import_command)
        #节点数量和关系数量
        node_count=0
        edge_count=0
        node_labels=[]#第一个字段是输入的lables，可能两个值，后面一个字段是明细
        edge_types=[]
        properties=[]#第一个字段是类型，第二个字段是输入的lables或者type，第三个字段是名称，第四个字段是类型
        start_import_time=datetime.datetime.now()
        for index in range(len(manage_import_data)):
            if manage_import_data[index]:
                item=import_data[index]
                #跟新数据库中的开始导入时间
                u_uuid=item['u_uuid']
                #print(u_uuid)
                import_data_db=db_session.query(ImportData).filter(ImportData.u_uuid==u_uuid).one()
                import_data_db.u_start_import_datetime=start_import_time
                #数据文件信息
                u_queue_uuid=item['u_queue_uuid']
                u_ndoe_edge=item['u_node_edge']
                u_queue_uuid=item['u_queue_uuid']
                u_label_items=''
                u_edge_type=''
                if u_ndoe_edge=='node':
                    #node
                    u_label_items=item['u_label_items'].split(',')
                    labels=''
                    for label in u_label_items:
                        labels+=':'+label
                        if [u_label_items,label] not in node_labels:
                            node_labels.append([u_label_items,label])
                    import_command+=' --nodes'+labels+'='+import_neo4j_install_dir.par_value+'import/'+u_queue_uuid
                    node_count+=import_data_db.u_rowcount
                    

                else:
                    #edge
                    u_edge_type=item['u_edge_type']
                    if u_edge_type not in edge_types:
                        edge_types.append(u_edge_type)
                    import_command+=' --relationships:'+u_edge_type+'='+import_neo4j_install_dir.par_value+'import/'+u_queue_uuid
                    edge_count+=import_data_db.u_rowcount
                #处理属性
                u_column_items=item['u_column_items']
                #print(u_column_items)
                #解析u_column_items为数组
                array_cols=u_column_items.split(',')
               
                flag=0
                while(flag<len(array_cols)):
                    col_item=[]
                    col_item.append(u_ndoe_edge)
                    col_item.append(str(u_label_items) if u_ndoe_edge=='node' else u_edge_type)
                    col_item.append(array_cols[flag])
                    flag+=1
                    #col_item.append(array_cols[flag])
                    flag+=1
                    col_item.append(array_cols[flag])
                    flag+=1
                    properties.append(col_item)
                    #print(col_item)


        db_session.commit()
        import_command+=' --ignore-extra-columns=true --ignore-missing-nodes=true --ignore-duplicate-nodes=true'
        
        #停止Neo4j
        socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'开始停止分析服务器'})
        #emit('neo4j_rebuild_process', {'message': '开始停止分析服务器'}, broadcast=True)
        stop_commonad=import_neo4j_install_dir.par_value+('bin/neo4j.bat' if system_type=='Windows' else 'bin/neo4j')+' stop'
        print(stop_commonad)
        r_stop_commonad = os.popen(stop_commonad).read()#subprocess.call(stop_commonad)
        print(r_stop_commonad)
        #socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'分析服务器成功停止'})
        #emit('neo4j_rebuild_process', {'message': '分析服务器成功停止'}, broadcast=True)
        #删除原数据库
        socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'开始清理服务器数据'})
        #emit('neo4j_rebuild_process', {'message': '开始清理服务器数据'}, broadcast=True)
        
        long_run(socketio,'clean_neo4j','')
        '''
        while True:
            mem=psutil.virtual_memory()
            disk=psutil.disk_usage(import_neo4j_install_dir.par_value)
            socketio.emit('system_report',{'platform':platform.platform(),'disk_total':disk.total,'disk_free':disk.free,'cpu_percent':psutil.cpu_percent(),'mem_total':mem.total,'mem_used':mem.used,'mem_free':mem.free}, broadcast=True)
            socketio.sleep(10)
            if system_type=='Windows':
                windows_path=import_neo4j_install_dir.par_value.replace("/", "\\")
                if os.path.exists(windows_path+'data\\databases\\graph.db\\temp.db\\temp.db'):
                    del_db_command='del /q '+windows_path+'data\\databases\\graph.db\\temp.db\\temp.db'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                if os.path.exists(windows_path+'data\\databases\\graph.db\\temp.db'):
                    del_db_command='del /q '+windows_path+'data\\databases\\graph.db\\temp.db'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                if os.path.exists(windows_path+'data\\databases\\graph.db\\index'):
                    del_db_command='del /q '+windows_path+'data\\databases\\graph.db\\index'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                if os.path.exists(windows_path+'data\\databases\\graph.db\\profiles'):
                    del_db_command='del /q '+windows_path+'data\\databases\\graph.db\\profiles'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                if os.path.exists(windows_path+'data\\databases\\graph.db'):
                    del_db_command='del /q '+windows_path+'data\\databases\\graph.db'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                #删除目录
                if os.path.exists(windows_path+'data\\databases\\graph.db\\temp.db\\temp.db'):
                    del_db_command='rd '+windows_path+'data\\databases\\graph.db\\temp.db\\temp.db'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                if os.path.exists(windows_path+'data\\databases\\graph.db\\temp.db'):
                    del_db_command='rd '+windows_path+'data\\databases\\graph.db\\temp.db'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                if os.path.exists(windows_path+'data\\databases\\graph.db\\index'):
                    del_db_command='rd '+windows_path+'data\\databases\\graph.db\\index'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                if os.path.exists(windows_path+'data\\databases\\graph.db\\profiles'):
                    del_db_command='rd '+windows_path+'data\\databases\\graph.db\\profiles'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                if os.path.exists(windows_path+'data\\databases\\graph.db'):
                    del_db_command='rd '+windows_path+'data\\databases\\graph.db'
                    print(del_db_command)
                    r_del_db_command = os.popen(del_db_command).read()
                    print(r_del_db_command)
                #测试是否删掉
                if os.path.exists(windows_path+'data\\databases\\graph.db'):
                    #数据库并未停止继续删除
                    pass
                else:
                    break

            else:
                del_db_command='rm -Rf '+import_neo4j_install_dir.par_value+'data/databases/graph.db'
                print(del_db_command)
                r_del_db_command = os.popen(del_db_command).read()
                print(r_del_db_command)
                #测试是否删掉
                if os.path.exists(import_neo4j_install_dir.par_value+'data/databases/graph.db'):
                    #数据库并未停止继续删除
                    pass
                else:
                    break
            
        '''    
        #socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'服务器数据成功清理'})
        #emit('neo4j_rebuild_process', {'message': '服务器数据成功清理'}, broadcast=True)
        #导入数据库
        socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'开始导入数据并重建分析数据库，请等待'})
        #emit('neo4j_rebuild_process', {'message': '开始导入数据并重建分析数据库，请等待'}, broadcast=True)
        
        #socketio.start_background_task(neo4j_import,{'import_command':import_command,'system_type':system_type,'properties':properties,'edge_types':edge_types,'node_labels':node_labels,'edge_count':edge_count,'node_count':node_count,'neo4j_import':neo4j_import, 'import_neo4j_install_dir':import_neo4j_install_dir.par_value,'manage_import_data':manage_import_data,'import_data':import_data})

        #发送任务到queue
        long_run(socketio,'import_data',import_command)

        '''
        import_queue_uuid=str(uuid.uuid1())
        import_queue=JobQueue(u_uuid=import_queue_uuid,u_declare_key='import_data',u_body=import_command,u_publisher_id='import_data',u_publish_datetime=start_import_time,u_no_ack=False,u_start_datetime=None,u_complete_datetime=None,u_status='发布')
        db_session.add(import_queue)
        db_session.flush()
        db_session.commit()

        #循环检测状态看是否导入成功
        db_session_check=create_session()
        import_queue_reload_init=db_session_check.query(JobQueue).filter(JobQueue.u_uuid==import_queue_uuid).one()
        u_complete_datetime=import_queue_reload_init.u_complete_datetime
        db_session_check.close()
        while u_complete_datetime==None:
            socketio.sleep(10)
            mem=psutil.virtual_memory()
            disk=psutil.disk_usage(import_neo4j_install_dir.par_value)
            
            socketio.emit('system_report',{'platform':platform.platform(),'disk_total':disk.total,'disk_free':disk.free,'cpu_percent':psutil.cpu_percent(),'mem_total':mem.total,'mem_used':mem.used,'mem_free':mem.free}, broadcast=True)
            db_session_check=create_session()
            import_queue_reload=db_session_check.query(JobQueue).filter(JobQueue.u_uuid==import_queue_uuid).one()
            u_complete_datetime=import_queue_reload.u_complete_datetime
            u_status=import_queue_reload.u_status
            db_session_check.close()
            print(import_queue_uuid)
            print(u_status)
            print(u_complete_datetime)
            
        '''
        socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'导入数据成功'})
        #emit('neo4j_rebuild_process', {'message': '导入数据成功'}, broadcast=True)
        socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'开始启动分析服务器'})
        #emit('neo4j_rebuild_process', {'message': '开始启动分析服务器'}, broadcast=True)
        
        #启动数据库
        start_commonad=import_neo4j_install_dir.par_value+('bin/neo4j.bat' if system_type=='Windows' else 'bin/neo4j')+' start'
        print(start_commonad)
        r_start_commonad = os.popen(start_commonad).read()#subprocess.call(start_commonad)

        #socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'分析服务器启动成功'})
        #emit('neo4j_rebuild_process', {'message': '分析服务器启动成功'}, broadcast=True)
        #socketio.sleep(5)
        print("分析服务器启动成功")

        socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_end", 'message_info':'分析数据库重建完成'})
        #emit('neo4j_rebuild_end', {'message': '分析数据库重建完成'}, broadcast=True)
        print("重建数据库完成")
        
        #跟新数据库数据
        end_import_time=datetime.datetime.now()
        #manage_import_data=par_dict['manage_import_data']
        #import_data=par_dict['import_data']
        for index in range(len(manage_import_data)):
            if manage_import_data[index]:
                item=import_data[index]
                u_uuid=item['u_uuid']
                import_data_db=db_session.query(ImportData).filter(ImportData.u_uuid==u_uuid).one()
                import_data_db.u_end_import_datetime=end_import_time
            #更新节点数量和关系数量
        node_count_db=db_session.query(SystemPar).filter(SystemPar.par_code=='node_count').one()
        #node_count=par_dict['node_count']
        node_count_db.par_value=str(node_count)
        edge_count_db=db_session.query(SystemPar).filter(SystemPar.par_code=='edge_count').one()
        #edge_count=par_dict['edge_count']
        edge_count_db.par_value=str(edge_count)
        db_session.flush()

            #更新数据库中现有的节点、关系和属性
        CurrentNodeLabels.delete_all(db_session)
        db_session.flush()
        #node_labels=par_dict['node_labels']
        for node_label in node_labels:

            currentNodeLabels=CurrentNodeLabels(labels=str(node_label[0]),label=node_label[1],create_datetime=end_import_time)
            db_session.add(currentNodeLabels)
        db_session.flush()
        CurrentEdgeTyps.delete_all(db_session)
        db_session.flush()
        #edge_types=par_dict['edge_types']
        for edge_type in edge_types:
            currentEdgeTyps=CurrentEdgeTyps(edge_type=edge_type,create_datetime=end_import_time)
            db_session.add(currentEdgeTyps)
            
        db_session.flush()
        CurrentProperties.delete_all(db_session)
        db_session.flush()
        #properties=par_dict['properties']
        for _property in properties:
            currentProperties=CurrentProperties(u_uuid=str(uuid.uuid1()),u_type=_property[0],u_label_type=_property[1],u_column_name=_property[2],u_column_type=_property[3],create_datetime=end_import_time)
            db_session.add(currentProperties)

        #设置其它数据的导入时间为NONE


        other_import_data_dbs=db_session.query(ImportData).filter(ImportData.u_end_import_datetime!=end_import_time).all()
        for item in other_import_data_dbs:
            #item=other_import_data_dbs[i]
            item.u_start_import_datetime=None
            item.u_end_import_datetime=None
        db_session.commit()
        db_session.close()

        

def long_time_process(messsage):
    
    #print(messsage['message_type'])
    socketio.emit(messsage['message_type'], messsage['message_info'], broadcast=True)


background_importing_thread_flag=True
def neo4j_import(par_dict):

    background_importing_thread_flag=True
    socketio.start_background_task(wait_for_import_end,par_dict)
    
    print(par_dict['import_command'])
    system_type=par_dict['system_type']
    socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':par_dict['import_command']})
    r_import_command= os.popen(par_dict['import_command']).read()#subprocess.call(import_command)
    background_importing_thread_flag=False
    
        #emit('neo4j_rebuild_process', {'message': r_import_command}, broadcast=True)
    

def wait_for_import_end(par_dict):
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        print("okokokoko")
        if background_importing_thread_flag:
            socketio.sleep(10)
            count += 1
            socketio.emit('system_report',psutil.cpu_times(), broadcast=True)
            print('background_thread_importing')
            print(count)
        else:
            print("background_thread_imported")
            break
    socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'导入数据成功'})
        #emit('neo4j_rebuild_process', {'message': '导入数据成功'}, broadcast=True)
    socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'开始启动分析服务器'})
        #emit('neo4j_rebuild_process', {'message': '开始启动分析服务器'}, broadcast=True)
        
        #启动数据库
    start_commonad=par_dict['import_neo4j_install_dir']+('bin/neo4j.bat' if system_type=='Windows' else 'bin/neo4j')+' start'
    print(start_commonad)
    r_start_commonad = os.popen(start_commonad).read()#subprocess.call(start_commonad)

    socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_process", 'message_info':'分析服务器启动成功'})
        #emit('neo4j_rebuild_process', {'message': '分析服务器启动成功'}, broadcast=True)
        #socketio.sleep(5)
    print("分析服务器启动成功")

    socketio.start_background_task(long_time_process,{'message_type':"neo4j_rebuild_end", 'message_info':'分析数据库重建完成'})
        #emit('neo4j_rebuild_end', {'message': '分析数据库重建完成'}, broadcast=True)
    print("重建数据库完成")
    db_session=create_session()
        #跟新数据库数据
    end_import_time=datetime.datetime.now()
    manage_import_data=par_dict['manage_import_data']
    import_data=par_dict['import_data']
    for index in range(len(manage_import_data)):
        if manage_import_data[index]:
            item=import_data[index]
            u_uuid=item['u_uuid']
            import_data_db=db_session.query(ImportData).filter(ImportData.u_uuid==u_uuid).one()
            import_data_db.u_end_import_datetime=end_import_time
        #更新节点数量和关系数量
    node_count_db=db_session.query(SystemPar).filter(SystemPar.par_code=='node_count').one()
    node_count=par_dict['node_count']
    node_count_db.par_value=str(node_count)
    edge_count_db=db_session.query(SystemPar).filter(SystemPar.par_code=='edge_count').one()
    edge_count=par_dict['edge_count']
    edge_count_db.par_value=str(edge_count)
    db_session.flush()

        #更新数据库中现有的节点、关系和属性
    CurrentNodeLabels.delete_all(db_session)
    db_session.flush()
    node_labels=par_dict['node_labels']
    for node_label in node_labels:

        currentNodeLabels=CurrentNodeLabels(labels=str(node_label[0]),label=node_label[1],create_datetime=end_import_time)
        db_session.add(currentNodeLabels)
    db_session.flush()
    CurrentEdgeTyps.delete_all(db_session)
    db_session.flush()
    edge_types=par_dict['edge_types']
    for edge_type in edge_types:
        currentEdgeTyps=CurrentEdgeTyps(edge_type=edge_type,create_datetime=end_import_time)
        db_session.add(currentEdgeTyps)
        
    db_session.flush()
    CurrentProperties.delete_all(db_session)
    db_session.flush()
    properties=par_dict['properties']
    for _property in properties:
        currentProperties=CurrentProperties(u_uuid=str(uuid.uuid1()),u_type=_property[0],u_label_type=_property[1],u_column_name=_property[2],u_column_type=_property[3],create_datetime=end_import_time)
        db_session.add(currentProperties)
    #设置其它的import_data的导入日期为NONE
    end_import_time
    db_session.commit()
    db_session.close()
        





@socketio.on('connect')
def test_connect():
    sid = request.sid
    print('Client connected'+sid)

    
    #socketio.start_background_task(target=background_thread)



@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')



if __name__=='__main__':  
    #app.debug = True
    #app.run(host='0.0.0.0')

    socketio.run(app,debug=True,host='0.0.0.0',port=5000)