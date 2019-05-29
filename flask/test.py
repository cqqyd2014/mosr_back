from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,jsonify
import json
from flask_cors import CORS
from orm import create_session,SystemPar,init_db,SystemCode,ProcessDetail,SystemData,QueryTemplate
from restful import TableRestful
import os
from neo4j import GraphDatabase
from neo4j_common import buildNodes,buildEdges,createNode,getPath,getJson,createEdge
import datetime
import uuid
import xlwings as xw

app=Flask(__name__)
CORS(app, resources=r'/*')
temp_dir="d:/temp/"

system_default_dir="D:/software/neo4j-community-3.5.3/"

@app.route('/systemstatus/')
def system_status():
    import win32file
    res_list = win32file.GetDiskFreeSpace(system_default_dir)
    disk_free_space = res_list[0]*res_list[1]*res_list[2]/(1024*1024.0)
    return jsonify({'free_space':disk_free_space,'system_default_dir':system_default_dir})

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
    print("start")
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
            print(create_string)
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
    print("start")
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
            print(create_string)
            row_flag+=1
        session.close()
    wb.close()
    app.quit()
    
    return jsonify({'status':'success'})

@app.route('/neo4jdata/')
def neo4j_data():
    if  'neo4jgraph_cypher' in request.args:
        return getPath(request.args['neo4jgraph_cypher'])
        
    else:
        pass


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
        post=db_session.query(SystemPar).filter(SystemPar.par_code==request.args['par_code']).one()
        db_session.close()
        return  jsonify(post.to_json())


    
@app.route('/neo4jJson/')
def neo4j_labels():
    if  'neo4jgraph_cypher' in request.args:
        #return getPath(request.args['neo4jgraph_cypher'])
        return getJson(request.args['neo4jgraph_cypher'])
        
    else:
        pass
    
    
        
    



@app.route('/SystemPar/',methods=['POST'])
def new_system_par():

    systemPar=SystemPar.from_json(request.json)
    db_session=create_session()
    db_session.add(systemPar)
    db_session.close()

@app.route('/SystemPar/',methods=['GET'])
def get_posts():
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
    print(request.get_json(silent=True))
    if not request.json :
        abort(400)
    processDetail=ProcessDetail(pd_uuid=str(uuid.uuid1()),pd_start_datetime=datetime.datetime.now(),pd_catalog=request.json['pd_catalog'],pd_command=request.json['pd_command'])
    db_session=create_session()
    db_session.add(processDetail)
    pd_json= processDetail.to_json()
    db_session.commit()
    db_session.close()
    return jsonify({'ProcessDetail':pd_json}), 201



@app.route('/SaveTemplate/',methods=['POST'])
def save_template():
    print(request.get_json(silent=True))
    if not request.json :
        abort(400)
    queryTemplate=QueryTemplate(qt_uuid=str(uuid.uuid1()),qt_datetime=datetime.datetime.now(),qt_object=request.json['qt_object'],qt_cypher=request.json['qt_cypher'],qt_title=request.json['qt_title'],qt_desc=request.json['qt_desc'])
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





if __name__=='__main__':  
    app.debug = True
    app.run(host='0.0.0.0')