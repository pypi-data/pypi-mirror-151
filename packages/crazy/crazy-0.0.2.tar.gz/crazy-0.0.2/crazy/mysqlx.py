import re
from crazy.dbx import DBx
from pymysql import Connection
from .table_dao import TableDao, RedisTableDao


def pick_values(m, keys):
    r = [None] * len(keys)
    for i, k in enumerate(keys):
        if k in m:
            r[i] = m[k]
    return r


class Mysqlx(DBx):

    def __init__(self, con: Connection):
        self.con: Connection = con

    def autocommit(self, value):
        self.con.autocommit(value)

    def close(self):
        self.con.close()

    def __enter__(self):
        self.con.begin()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print(exc_tb)
            self.con.rollback()
        else:
            self.con.commit()

    def get(self, table: str, id, id_field='id'):
        sql = "select * from " + self.escape_table(table) + " where " + self.escape_field(
            id_field) + "=%s "
        return self.query_one(sql, (id,))

    def get_by_keys(self, table: str, append_sql: str = None, **kwargs):
        sql = "select * from " + self.escape_table(table) + " where " + self.sql_keys_condition(
            kwargs.keys())
        if append_sql:
            sql += " " + append_sql
        return self.query_one(sql, list(kwargs.values()))

    def list(self, table: str, ids: [], id_field='id'):
        sql = "select * from " + self.escape_table(table) + " where " + self.escape_field(
            id_field) + " in (" \
              + self.sql_holds(len(ids), "%s") + ")"
        # if append_sql:
        #     sql += " " + append_sql
        return self.query(sql, ids)

    def list_by_keys(self, table: str, append_sql: str = None, **kwargs):
        sql = "select * from " + self.escape_table(table) + " where " + self.sql_keys_condition(
            kwargs.keys())
        if append_sql:
            sql += " " + append_sql
        return self.query(sql, list(kwargs.values()))

    def query(self, sql: str, args=None) -> [dict]:
        sql, args = self.translate_named_sql(sql, args)
        with self.con.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchall()

    def query_one(self, sql: str, args=None) -> [dict]:
        sql, args = self.translate_named_sql(sql, args)
        with self.con.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchone()

    def query_value(self, sql: str, args=None):
        r = self.query_one(sql, args)
        if r is None:
            return None
        if len(r) > 0:
            if len(r) > 1:
                print("warning: BaseDbWrap.query_value there are many value in result.", r)
            for k in r:
                return r[k]

    def insert(self, table, record: dict):
        sql = self.make_insert_sql(table, record)
        with self.con.cursor() as cursor:
            cursor.execute(sql, tuple(record.values()))
            return cursor.lastrowid

    def update(self, table: str, params: dict, id_field: str = 'id'):
        id_value = params[id_field]
        update_params = {k: v for k, v in params.items() if k != id_field}
        sql = self.make_update_sql(table, update_params, id_field)
        with self.con.cursor() as cursor:
            return cursor.execute(sql, list(update_params.values()) + [id_value])

    def delete(self, table, id, id_field: str = 'id'):
        sql = self.make_delete_sql(table, id_field)
        with self.con.cursor() as cursor:
            return cursor.execute(sql, (id,))

    def execute(self, sql, params):
        with self.con.cursor() as cursor:
            if type(params) == dict:
                tsql, args = self.translate_named_sql(sql, params)
                return cursor.execute(tsql, args)
            return cursor.execute(sql, params)

    def save(self, table: str, record: dict, update_keys: [str]):
        args = list(record.values())
        if not update_keys:
            sql = self.make_insert_sql(table, record, True)
            return self.execute(sql, args)
        sql = self.make_insert_sql(table, record, False)
        sql += " on duplicate key update "
        sql += self.sql_keys_update(update_keys)
        args = args + pick_values(record, update_keys)
        with self.con.cursor() as cursor:
            cursor.execute(sql, args)
            id = cursor.lastrowid
            if id == 0:
                return self.get_by_keys(table, {k: record[k] for k in update_keys})

    def translate_named_sql(self, named_sql, args: dict, pattern=r":(\w+)") -> (str, []):
        if dict != type(args):
            return named_sql, args
        result = []

        def repl(m) -> str:
            k = m.group(1)
            if k in args:
                result.append(args[k])
                return '%s'
            else:
                return m.group(0)

        return re.sub(pattern, repl, named_sql), result

    def escape_table(self, table: str) -> str:
        return '`' + table + '`'

    def escape_field(self, field: str) -> str:
        return '`' + field + '`'

    def make_insert_sql(self, table: str, record: dict, ignore=False):
        return f"insert {'ignore' if ignore else 'into'} " + self.escape_table(table) + " (" + self.sql_fields(
            record.keys()) + ") values (" + self.sql_holds(len(record)) + ")"

    def make_update_sql(self, table: str, param: dict, id_field="id"):
        return "update " + self.escape_table(table) + " set " + self.sql_keys_update(
            param.keys()) + " where " + self.escape_field(id_field) + "=%s"

    def make_delete_sql(self, table, id_field):
        return "delete from " + self.escape_table(table) + " where " + self.escape_field(id_field) + "=%s"

    def sql_holds(self, n, hold="%s"):
        """
        :param n: 2
        :param hold: %s
        :return: %s,%s
        """
        return ','.join([hold] * n)

    def sql_keys_condition(self, fields):
        """
        :param keys: eg.['name','age']
        :return: `name`=%s and `age`=%s
        """
        if not fields:
            return "", []
        sql = ""
        for f in fields:
            sql += self.escape_field(f) + "=%s and "
        return sql[:len(sql) - 5]

    def sql_keys_update(self, fields):
        """
        :param keys: eg.['name','age']
        :return: `name`=%s,`age`=%s
        """
        if not fields:
            return "", []
        sql = ""
        for k in fields:
            sql += self.escape_field(k) + '=%s,'
        return sql[:len(sql) - 1]

    def sql_fields(self, fields):
        """
        :param fields: eg.['name','age']
        :return: `name`,`age`
        """
        return ",".join([self.escape_field(f) for f in fields])

    def table_dao(self, table: str, id_field='id') -> TableDao:
        return TableDao(self, table, id_field)

    def redis_table_dao(self, redisx, table: str, id_field='id', redis_ttl: int = 1800,
                        redis_key_prefix: str = "", keys: [[]] = None) -> RedisTableDao:
        return RedisTableDao(redisx, self, table, id_field, redis_ttl=redis_ttl, redis_key_prefix=redis_key_prefix,
                             keys=keys)
