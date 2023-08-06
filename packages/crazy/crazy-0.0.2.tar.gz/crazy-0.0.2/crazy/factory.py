from functools import wraps
from abc import abstractmethod
import redis
from crazy.dbx import DBx
from crazy.redisx import Redisx
from crazy.mysqlx import Mysqlx
from typing import Sequence, Dict, Callable, AnyStr
import pymysql


class Pool:
    @abstractmethod
    def create(self):
        pass


class MysqlPool(Pool):

    def __init__(self, host: str, port: int, user: str, password: str, database: str, autocommit: bool = True,
                 cursorclass=None,
                 **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.autocommit = autocommit
        self.cursorclass = cursorclass or pymysql.cursors.DictCursor
        self.kwargs = kwargs

    def create(self):
        return pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                               database=self.database, autocommit=self.autocommit,
                               cursorclass=self.cursorclass, **self.kwargs)


class RedisPool(Pool):
    def __init__(self, url=None, host: str = None, port: int = 6379, db=0, password: str = None, **kwargs):
        """
        use url or the params(host,port,db,password) to create RedisPool
        :param url: redis://[[username]:[password]]@localhost:6379/0
        """
        if url is not None:
            self.pool = redis.ConnectionPool.from_url(url, **kwargs)
        else:
            self.pool = redis.ConnectionPool(host=host, port=port, db=db, password=password, **kwargs)

    def create(self):
        return Redisx(connection_pool=self.pool)


def injection_factory(pools: dict, dbxs: dict):
    """
    example:
    pools = {
        'mysql': create_mysql_pool(host,user,password,...)
        'redis': create_redis_pool(host,user,password,...)
    }
    dbx :{
        'mysql': Mysqlx,
        'redis'': Redisx,
    }

    db = con_injection_factory(pools, dbx)

    @db
    def query(mysql:Mysqlx=None):
        u = mysql.get('user',1)


    :param pools: {"mysql" : con_factory} con = con_factory.create()
    :param dbxs: eg.{pymysql: MysqlWrap} dbx(con), wrap created connections
    :return: injection object
    """

    def injection(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cons = []
            varnames = func.__code__.co_varnames
            for varname in varnames:
                if varname in pools:
                    if varname not in kwargs or not kwargs:
                        con = pools[varname].create()  # create new connection from datasource
                        if varname in dbxs:
                            con = dbxs[varname](con)
                        kwargs[varname] = con
                        cons.append(con)
            try:
                result = func(*args, **kwargs)
            finally:
                for con in cons:
                    con.close()  # connection should have close method
            return result

        return wrapper

    return injection
