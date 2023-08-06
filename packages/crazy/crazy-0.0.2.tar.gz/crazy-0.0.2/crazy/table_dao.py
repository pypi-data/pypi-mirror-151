from crazy.dbx import DBx
# from crazy.mysqlx import Mysqlx
from crazy.redisx import Redisx
from crazy.table_update_listener import table_listener


class TableDao:

    def __init__(self, dbx: DBx, table: str, id_field: str = "id"):
        self.table = table
        self.dbx = dbx
        self.id_field = id_field

    def insert(self, record: dict):
        return self.dbx.insert(self.table, record)

    def delete(self, id):
        return self.dbx.delete(self.table, id, self.id_field)

    def update(self, params):
        return self.dbx.update(self.table, params, self.id_field)

    def get(self, id) -> dict:
        return self.dbx.get(self.table, id)

    def get_by_keys(self, append_sql: str = None, **kwargs) -> dict:
        return self.dbx.get_by_keys(self.table, append_sql=append_sql, **kwargs)

    def list(self, ids: []) -> [dict]:
        return self.dbx.list(self.table, ids)

    def list_as_map(self, ids: []) -> dict:
        r = self.list(ids)
        if not r:
            return {}
        return {v[self.id_field]: v for v in r}

    def list_by_keys(self, append_sql: str = None, **kwargs) -> [dict]:
        return self.dbx.list_by_keys(self.table,append_sql=append_sql, **kwargs)


def redis_key(table, *kvs, prefix=""):
    return prefix + table + "/" + "/".join([str(v) for v in kvs])


class RedisTableDao(TableDao):

    def __init__(self, redisx: Redisx, dbx, table: str, id_field: str = "id", redis_ttl: int = 1800,
                 redis_key_prefix: str = "", keys: [[]] = None):
        super(RedisTableDao, self).__init__(dbx, table, id_field)
        self.redisx = redisx
        self.redis_ttl = redis_ttl
        self.redis_key_prefix = redis_key_prefix
        self.keys = set([])
        if keys is not None:
            self.keys = set(tuple(v) for v in keys)

    def redis_key(self, *args):
        return redis_key(self.table, *args, prefix=self.redis_key_prefix)

    def redis_key_dict(self, dict_args: dict):
        keys = sorted(dict_args.keys())
        args = [None] * (2 * len(keys))
        for i in range(len(keys)):
            args[2 * i] = keys[i]
            args[2 * i + 1] = dict_args[keys[i]]
        return redis_key(self.table, *args, prefix=self.redis_key_prefix)

    def get(self, id):
        rk = self.redis_key(self.id_field, id)
        obj = self.redisx.get_obj(rk)
        if obj is not None:
            return obj
        obj = super().get(id)
        self.redisx.set_obj(rk, obj, ex=self.redis_ttl)
        return obj

    def get_by_keys(self, append_sql: str = None, **kwargs) -> dict:
        """
        redis_key -> id -> obj
        :param kvs:
        :param append_sql:
        :param id_field:
        :param fields:
        :return:
        """
        if tuple(kwargs.keys()) not in self.keys:
            print("WARN: get_by_keys kv not in keys")
            return super().get_by_keys(append_sql=append_sql, **kwargs)
        rk = self.redis_key_dict(kwargs)
        id_value = self.redisx.get_obj(rk)
        if id_value is not None:
            return self.get(id_value)
        obj = super().get_by_keys(append_sql=append_sql, **kwargs)
        self.redisx.set_obj(rk, obj[self.id_field], ex=self.redis_ttl)
        return obj

    def list(self, ids: []):
        rks = [self.redis_key(self.id_field, v) for v in ids]
        objs = self.redisx.mget_obj(rks)
        objs = [v for v in objs if v is not None]
        if len(ids) == len(objs):
            return objs
        miss_ids = set(ids) - set([v[self.id_field] for v in objs])
        miss_objs = super().list(miss_ids)
        self.redisx.mset_obj(miss_objs, lambda v: self.redis_key(self.id_field, v[self.id_field]), self.redis_ttl)
        return objs + miss_objs

    def list_by_keys(self, append_sql: str = None, **kwargs) -> [{}]:
        """
        redis_key ->[id] ->objs
        :param kv:
        :param append_sql:
        :return:
        """
        if tuple(kwargs.keys()) not in self.keys:
            print("WARN: get_by_keys kv not in keys")
            return super().list_by_keys(append_sql=append_sql, **kwargs)
        rk = self.redis_key_dict(kwargs)
        id_values = self.redisx.get_obj(rk)
        if id_values is not None:
            return self.list(id_values)
        objs = super().list_by_keys(append_sql=append_sql, **kwargs)
        self.redisx.set_obj(rk, [obj[self.id_field] for obj in objs], ex=self.redis_ttl)
        return objs

    def clear_cache(self, id, kvs: [dict] = None):
        """
        delete cache by id
        :param id:
        :param kvs: [{k1:v1,k2:v2}]
        :return:
        """
        # self.redisx.delete(self.redis_key(self.id_field, id))
        rks = [self.redis_key(self.id_field, id)]
        table_listener.trigger_table_update(self.table, id)
        if kvs:
            for d in kvs:
                rks.append(self.redis_key_dict(d))
        if len(rks) > 0:
            self.redisx.delete(*rks)

    def _get_cached_kvs(self, record: dict):
        return [{k: record[k] for k in v} for v in self.keys]

    def insert(self, record: dict):
        id = super().insert(record)
        self.clear_cache(id, self._get_cached_kvs(record))
        return id

    def update(self, params: dict):
        id = params[self.id_field]
        old = super().get(id)
        rks = None
        if old:
            rks = self._get_cached_kvs(old)
        super().update(params)
        self.clear_cache(id, rks)
        return id

    def delete(self, id):
        old = super().get(id)
        rks = None
        if old:
            rks = self._get_cached_kvs(old)
        super().delete(id)
        self.clear_cache(id, rks)
        return id
