from orm import create_session,SystemPar,init_db,SystemCode

db_session=create_session()
init_db(db_session)
db_session.close()