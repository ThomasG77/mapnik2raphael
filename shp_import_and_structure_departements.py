#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.spatialite_sqlite import *
from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
from contextlib import closing
import os

cur = conn.cursor()
shppath = os.getcwd()

with closing(cur):
    #import ipdb; ipdb.set_trace() # Reminder for debugging

    # Initialize spatial table
    init_spatialdb(cur)

    # Testing library versions
    rs = cur.execute('SELECT sqlite_version(), spatialite_version()')
    for value in rs:
        msg = "> SQLite v%s Spatialite v%s" % (value[0], value[1])
        print msg

    if shpfile + ".shp"  in os.listdir(os.getcwd()):
        # Import shp
        import_shp(conn, tablename, os.path.join(shppath, shpfile), coding, prj, "MULTIPOLYGON")

        # Just see if some contents
        print showquery(cur, 'SELECT "CODE_DEPT", lower(NOM_DEPT) as NOM_DEPT, "CODE_CHF", "NOM_CHF" \
            FROM "departements" LIMIT 10')

