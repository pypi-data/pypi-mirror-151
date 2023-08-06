from abc import abstractmethod
from typing import Sequence, Dict, Callable


class DBx:
    """
    database client wrap
    """

    def autocommit(self, value):
        pass

    def close(self):
        pass

    def get(self, table: str, id, id_field='id'):
        pass

    def get_by_keys(self, table: str, append_sql: str = None, **kwargs):
        pass

    def list(self, table: str, ids: [], id_field='id'):
        pass

    def list_by_keys(self, table: str, append_sql: str = None, **kwargs):
        pass

    def query(self, sql: str, args=None) -> [dict]:
        pass

    def query_one(self, sql: str, args=None) -> [dict]:
        pass

    def query_value(self, sql: str, args=None):
        pass

    def insert(self, table, record: dict):
        pass

    def update(self, table: str, params: dict, id_field: str = 'id'):
        pass

    def delete(self, table, id, id_field: str = 'id'):
        pass
    def execute(self, sql , params):
        pass

    # def save(self, table: str, record: dict, update_keys: [str]):
    #     args = list(record.values())
    #     if not update_keys:
    #         sql = self.make_insert_sql(table, record, True)
    #         return self.execute(sql, args)
    #     sql = self.make_insert_sql(table, record, False)
    #     sql += " on duplicate key update "
    #     sql += self.sql_keys_update(update_keys)
    #     args = args + pick_values(record, update_keys)
    #     with self.con.cursor() as cursor:
    #         print(sql , args)
    #         cursor.execute(sql, args)
    #         id = cursor.lastrowid
    #         if id == 0:
    #             return self.get_by_keys(table, {k: record[k] for k in update_keys})

    def translate_named_sql(self, named_sql, args: dict, pattern=r":(\w+)") -> (str, []):
        pass

    def escape_table(self, table: str) -> str:
        return '`' + table + '`'

    def escape_field(self, field: str) -> str:
        return '`' + field + '`'
