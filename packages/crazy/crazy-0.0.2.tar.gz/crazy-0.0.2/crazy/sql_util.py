def append_sql(args: [], name: str, value, op='=') -> str:
    if value is not None:
        args.append(value)
        return f" and `{name}` {op} %s "
    return ""


def append_in(args, name: str, values: []) -> str:
    if values is not None:
        for v in values:
            args.append(v)
        return f" and `{name}` in (" + (','.join(['%s'] * len(values))) + ")"
    return ""


def append_named_sql(name, op='=') -> str:
    return f" and `{name}` {op} :{name} "


def join_ints(ints: [int]) -> str:
    if not ints:
        return "(null)"
    return ','.join([str(int(v)) for v in ints])

