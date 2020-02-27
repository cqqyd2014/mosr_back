
#from flask import current_app, g
import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO


from .db import close_flask_db


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
   
    

   

    #蓝图
   

    
    from system import flask_route as system_route
    app.register_blueprint(system_route.system)
   
    
    app.teardown_appcontext(close_flask_db)

    

    
    


    return app



if __name__ == "__main__":
    import os

    flask_env_production_or_development = os.environ.get("FLASK_ENV", default="production")
    app=create_app()
    
    app.config['session_save_to_mem_or_database']=os.environ.get("SESSION_SAVE_TO_MEM_OR_DATABASE", default="MEM")
    socketio = SocketIO(app,cors_allowed_origins='*')
    #socketio.init_app(app)
    from system import connect_event,disconnect_event

    socketio.on_event('connect', connect_event,namespace='/system')
    socketio.on_event('disconnect',disconnect_event,namespace='/system')

    if flask_env_production_or_development=='production':
        socketio.run(app,debug=False,host='0.0.0.0',port=5000)
    else:
        
        socketio.run(app,debug=True,host='0.0.0.0',port=5000)
    
    
    

