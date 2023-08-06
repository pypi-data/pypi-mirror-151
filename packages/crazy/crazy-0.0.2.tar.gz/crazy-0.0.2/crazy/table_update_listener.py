class _TableUpdateListener:

    """
    table -> [dependency_fn]
    """

    def __init__(self):
        self.table_deps = {}

    def add(self, table, callback):
        if table not in self.table_deps:
            self.table_deps[table] = [callback]
        else:
            self.table_deps[table].append(callback)

    def trigger_table_update(self, table, id):
        if table in self.table_deps:
            for fn in self.table_deps[table]:
                fn(table, id)

    def on_update(self, table):
        def wrap(fn):
            self.add(table, fn)
            return fn
        return wrap


table_listener = _TableUpdateListener()
