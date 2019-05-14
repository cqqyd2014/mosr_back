from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,jsonify
import json
from flask_cors import CORS
from orm import create_session,SystemPar,init_db,SystemCode,ProcessDetail
from restful import TableRestful


app=Flask(__name__)
CORS(app, resources=r'/*')
empty = []


@app.route('/')
def show_entries():
    user_agent=request.headers.get('User_Agent')
    return 'user_agent is %s' %user_agent


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)



@app.route('/SystemPar/',methods=['POST'])
def new_system_par():
    print(request.json)
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
        

@app.route('/SystemCode/',methods=['GET'])
def get_systemcodes():
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
        
        return jsonify(post.to_json())



@app.route('/ProcessDetail/',methods=['GET'])
def get_process_detail():

    class Process_detail(TableRestful):
        def __init__(self,args,db_session):
            super(Process_detail, self).__init__(args,db_session)
            self.query=self.db_session.query(ProcessDetail)

        def _query_parmeter(self):
            if 'start_datetime_begin' in self.args and 'start_datetime_end' in self.args:
                self.q_filter=self.query.filter(ProcessDetail.start_datetime >=request.args['start_datetime_begin'],ProcessDetail.start_datetime <=request.args['start_datetime_end'])
            else:
                self.q_filter=self.query
        
        def _ordery_by(self):
            self.q_order=self.q_filter.order_by(ProcessDetail.pd_start_datetime.desc())
    db_session=create_session()
    pd=Process_detail(request.args,db_session)
    rs=pd.get_rs_all()
    for r in rs:
        empty.append(r.to_json())
    db_session.close()
    return jsonify(empty)



if __name__=='__main__':  
    app.debug = True
    app.run(host='0.0.0.0')