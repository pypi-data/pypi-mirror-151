import redis
from typing import Any
from abc import abstractmethod

import pickle


class Serializer:
    @abstractmethod
    def dumps(self, obj: Any) -> bytes:
        pass

    @abstractmethod
    def loads(self, data: bytes) -> Any:
        pass


class PickleSerializer(Serializer):

    def dumps(self, obj: Any) -> bytes:
        return pickle.dumps(obj)

    def loads(self, data: bytes) -> Any:
        return pickle.loads(data)


class Redisx(redis.Redis):

    def __init__(self, serializer: Serializer = PickleSerializer(),*args, **kwargs):
        super(Redisx, self).__init__(*args, **kwargs)
        self.serializer = serializer

    def set_obj(self, key, obj, ex=None, px=None, nx=False, xx=False, keepttl=False):
        return self.set(key, self.serializer.dumps(obj), ex, px, nx, xx, keepttl)

    def get_obj(self, key):
        r = self.get(key)
        if r is None:
            return None
        return self.serializer.loads(r)


    def mget_obj(self, keys):
        if not keys:
            return
        rs = self.mget(keys)
        return [self.serializer.loads(r) for r in rs]

    def mset_obj(self, objs, key_fn, ex=0):
        if not objs:
            return
        kvs = [None] * len(objs)
        for i, v in enumerate(objs):
            kvs[2 * i] = key_fn(v)
            kvs[2 * i + 1] = self.serializer.dumps(v)
        self.mset(*kvs)
        if ex > 0:
            for i in range(0, len(kvs), 2):
                self.expire(kvs[i], ex)

    def hget_obj(self, name, key):
        return self.serializer.loads(self.hget(name, key))

    def hset_obj(self, name, key, value):
        return self.hset(name, key, self.serializer.dumps(value))

    def hgetall_obj(self, name):
        raw = self.hgetall(name)
        r = {}
        for k, v in raw:
            r[k] = self.serializer.loads(v)
        return r