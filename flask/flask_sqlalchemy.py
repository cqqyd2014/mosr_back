from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['postgresql://postgres:Wangli1980@localhost:33133/test']
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)