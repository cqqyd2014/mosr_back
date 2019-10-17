
from flask import current_app, g
import os
from flask import Flask
from database import *


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    from .root import root_bp
    app.register_blueprint(root_bp)

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
    from net_tyc import flask_route
    app.register_blueprint(flask_route.bp)

    return app

