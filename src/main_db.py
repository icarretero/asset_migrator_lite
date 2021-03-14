from src.maria_db import MariaDB, MariaDBException


class MainDBException(Exception):
    pass


class MainDB:

    DB_NAME = "assets"
    TABLE_NAME = "assets"
    ID_KEY = "entry_id"
    PATH_KEY = "path"

    def __init__(self):
        try:
            self.database = MariaDB(self.DB_NAME)
        except MariaDBException as e:
            raise MainDBException(
                "Database Error performing connection"
            ) from e

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
        try:
            jobs = self.database.select(query)
        except MariaDBException as e:
            raise MainDBException(
                "DataBase Error performing query"
            ) from e
        return jobs

    def update_jobs(self):
        pass
