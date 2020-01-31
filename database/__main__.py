

from database.initdb_run import init_db
from . import get_db


if __name__ == "__main__":
    
    db_session=get_db()
    print('Initialized the database start.')
    init_db(db_session)
    print('Initialized the database compelet.')
