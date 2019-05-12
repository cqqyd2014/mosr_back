from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,jsonify

from orm import create_session,SystemPar,init_db

app=Flask(__name__)

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
    db_session=create_session()
    posts=db_session.query(SystemPar).all()
    json_object=jsonify({'system_par':[post.to_json() for post in posts]})
    db_session.close()
    return json_object
 
@app.route('/SystemPar/<string:id>',methods=['GET'])
def get_post(id):
    db_session=create_session()
    post=db_session.query(SystemPar).filter(SystemPar.par_code==id).one()
    db_session.close()
    return  jsonify(post.to_json())



if __name__=='__main__':
    db_session=create_session()
    init_db(db_session)
    app.debug = True
    app.run(host='0.0.0.0')