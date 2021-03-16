from src.maria_db import (
    MariaDB,
    MariaDBException,
    MariaDBConnectionError
)


class MainDBException(Exception):
    pass


class MainDBConnectionError(MainDBException):
    pass


def handle_exceptions(method):
    def wrapper(*v, **kw):
        try:
            return method(*v, **kw)
        except MariaDBConnectionError as e:
            raise MainDBConnectionError(e)
        except MariaDBException as e:
            raise MariaDBException("Unhandled DB error") from e
    return wrapper


class MainDB:

    DB_NAME = "assets"
    TABLE_NAME = "assets"
    ID_KEY = "entry_id"
    PATH_KEY = "path"

    def __init__(self):
        self._create_db()

    @handle_exceptions
    def _create_db(self):
        self.database = MariaDB(self.DB_NAME)

    @handle_exceptions
    def get_batch_from_id_with_prefix(self, batch_size, _id, prefix):
        query = (
            "SELECT {id_key}, {path_key} "
            "FROM {table_name} "
            "WHERE {path_key} like '{prefix}/%' "
            "AND {id_key} > {_id} "
            "LIMIT {batch_size} ;"
        ).format(
            id_key=self.ID_KEY,
            path_key=self.PATH_KEY,
            table_name=self.TABLE_NAME,
            prefix=prefix,
            batch_size=batch_size,
            _id=_id
        )
        jobs = self.database.select(query)
        return jobs

    @handle_exceptions
    def update_path(self, _id, path):
        query = (
            # "UPDATE LOW_PRIORITY {table_name} "
            "UPDATE {table_name} "
            "SET {path_key}='{path}' "
            "WHERE {id_key} = {_id}; "
        ).format(
            id_key=self.ID_KEY,
            path_key=self.PATH_KEY,
            table_name=self.TABLE_NAME,
            path=path,
            _id=_id
        )
        self.database.update(query)
