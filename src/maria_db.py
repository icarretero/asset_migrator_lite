import mariadb
import os


class MariaDBException(Exception):
    pass


class MariaDB():

    USER = os.getenv('MYSQL_USER', 'root')
    PWD = os.getenv('MYSQL_PWD')
    DATABASE = "assets"
    HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    PORT = os.getenv('MYSQL_PORT', 3306)

    def __init__(self, db_name):
        self.conn = self._get_connection(db_name)
        self.cursor = self._get_cursor()

    def _get_connection(self, db_name):
        try:
            conn = mariadb.connect(
                user=self.USER,
                password=self.PWD,
                host=self.HOST,
                port=self.PORT,
                database=db_name,
            )
        except mariadb.Error as e:
            raise MariaDBException(e)
        return conn

    def _get_cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def select(self, query):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
        except mariadb.Error as e:
            raise MariaDBException(e)
        return results
