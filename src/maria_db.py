import mariadb
import os


class MariaDBException(Exception):
    pass


class MariaDBConnectionError(MariaDBException):
    def __init__(self, message):
        message = "Error establishing connection with DB -> {message}".format(
            message=message
        )
        super().__init__(message)


def handle_exceptions(method):
    def wrapper(*v, **kw):
        try:
            return method(*v, **kw)
        except mariadb.OperationalError as e:
            raise MariaDBConnectionError(e)
        except mariadb.Error as e:
            raise MariaDBException(e)
    return wrapper


class MariaDB():

    USER = os.getenv('MYSQL_USER', 'root')
    PWD = os.getenv('MYSQL_PWD')
    HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    PORT = os.getenv('MYSQL_PORT', 3306)

    def __init__(self, db_name):
        self.conn = self._get_connection(db_name)
        self.cursor = self._get_cursor()

    @handle_exceptions
    def _get_connection(self, db_name):
        conn = mariadb.connect(
            user=self.USER,
            password=self.PWD,
            host=self.HOST,
            port=self.PORT,
            database=db_name,
        )
        return conn

    def _get_cursor(self):
        return self.conn.cursor()

    @handle_exceptions
    def close(self):
        self.conn.close()

    @handle_exceptions
    def select(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    @handle_exceptions
    def update(self, query):
        self.cursor.execute(query)
        self.conn.commit()
