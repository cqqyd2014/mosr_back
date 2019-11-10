
from flask import current_app, g
import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from database import *
from . import db


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources=r'/*')


    app.config.from_envvar('XYWL2019_SETTINGS')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #注册命令行
    from database import initdb_run
    initdb_run.init_app(app)
    from back_queue import main_run
    main_run.init_app(app)

    ##
    from chongqingzixun import read_attach
    read_attach.init_app(app)

    #蓝图
    from net_tyc import flask_route as net_tyc_route
    app.register_blueprint(net_tyc_route.bp)

    from bank import flask_route as bank_route
    app.register_blueprint(bank_route.bank)

    from system import flask_route as system_route
    app.register_blueprint(system_route)
   


    app.teardown_appcontext(db.close_flask_db)

    

    
    


    return app



if __name__ == "__main__":
    import os

    flask_env_production_or_development = os.environ.get("FLASK_ENV", default="production")
    
    app=create_app()
    socketio = SocketIO()
    socketio.init_app(app)
    from system import flask_socket as system_socket

    socketio.on_event('connect_event', system_socket.connect_event, namespace='/system_socket')

    if flask_env_production_or_development=='production':
        socketio.run(app,debug=False,host='0.0.0.0',port=5000)
    else:
        print(flask_env_production_or_development)
        socketio.run(app,debug=True,host='0.0.0.0',port=5000)
    
    

