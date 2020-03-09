import configparser
conf = configparser.ConfigParser()
conf.sections()
conf.read('db_config.ini')
hbase_ip=conf['Hbase']["Db_ip"]