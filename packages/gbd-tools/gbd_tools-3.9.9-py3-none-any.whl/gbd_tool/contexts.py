from gbd_tool.gbd_api import GBD, GBDException

from gbd_tool import config

import sqlite3

def merge(api: GBD, source, target):
    if not source in config.contexts():
        raise GBDException("source context not found: " + source)
    if not target in config.contexts():
        raise GBDException("target context not found: " + target)
    db = api.database
    trans = "{}_to_{}".format(target, source)
    tables = set([ db.ftable(f) for f in db.get_features() if db.fcontext(f) == target and not db.fvirtual(f) and f != trans ])
    print("trans ", trans)
    print("tfeat ", str(tables))
    for res in api.query_search(resolve=[trans]):
        [target, source] = res
        if target != None and source != None and target != source:
            if len(source.split(",")) > 2:
                print("strange case: " + str(res))
                continue
            if len(source.split(",")) > 1:
                [one, two] = source.split(",")
                source = one if one != target else two
            if target != source:
                for table in tables:
                    try:
                        db.execute("UPDATE {} SET hash='{}' WHERE hash='{}'".format(table, source, target))
                    except sqlite3.IntegrityError:
                        print("not updated ", target, " with ", source)
                    if db.cursor.rowcount:
                        print("updated ", target, " with ", source)
    