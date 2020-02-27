#初始化数据库


from . import get_db,init_db


if __name__ == "__main__":
    
    db_session=get_db()
    print('Initialized the xywl2019 database start.')
    init_db(db_session)
    print('Initialized the xywl2019 database compelet.')
    
    
