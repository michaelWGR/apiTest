import pymysql
from common import get_conf
from httprunner import logger

config = get_conf('DATABASE')


class MyDB(object):
    def __init__(self):
        self.config = config
        self.logger = logger
        self.db = None
        self.cursor = None

    def connectDB(self, database='i61-hll-manager', host='10.60.7.62'):
        '''连接数据库'''
        try:
            self.config['database'] = database
            self.config['host'] = host
            self.db = pymysql.connect(**self.config)
            self.cursor = self.db.cursor()
            print('Connect DB successfully')

        except ConnectionError as ex:
            print('DB connectton fail ')
            self.logger.log_error(str(ex))

    def executeSQL(self, sql):
        # 执行sql语句
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor

        except Exception as ex:
            print('sql execution fail')
            self.db.rollback()
            self.logger.log_error(str(ex))

    def get_all(self, cursor):
        # 获取执行完sql后返回的所有查询数据，返回tuple
        try:
            value = cursor.fetchall()
            return value

        except Exception as ex:
            print('fail to get data')
            self.logger.log_error(str(ex))

    def get_one(self, cursor):
        # 获取执行完sql后返回一条查询数据
        try:
            value = cursor.fetchone()
            return value

        except Exception as ex:
            print('fail to get data')
            self.logger.log_error(str(ex))

    def closeDB(self):
        # 关闭数据库连接
        try:
            self.db.close()
            print('Databased closed')

        except Exception as ex:
            print('fail to close DB')
            self.logger.log_error(str(ex))


if __name__ == '__main__':
    # mydb = MyDB()
    # mydb.connectDB()
    # sql = r'select * from `call_record`'
    # cursor = mydb.executeSQL(sql)
    # v = mydb.get_one(cursor)
    # print(v)
    # print(type(v))
    # mydb.closeDB()
    # e = get_os_environ('test')
    print(config)

