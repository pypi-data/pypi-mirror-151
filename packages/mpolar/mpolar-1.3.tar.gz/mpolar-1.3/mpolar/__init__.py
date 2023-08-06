from mpolar import table_format, list_format, polar


def parse(path: str, sep: str = ";", **kwargs):
    try:
        retval = table_format.parse(path, sep, **kwargs)
    except:
        retval = list_format.parse(path, sep)
    return retval


from mpolar import propulsion
