#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.spatialite_sqlite import *
from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
cur = conn.cursor()
import os
from contextlib import closing

with closing(cur):
    # Create table for importing csv
    cur.execute('CREATE TABLE IF NOT EXISTS pop_dept(idDept TEXT, nomDept TEXT, pop_2009_dept INTEGER, PRIMARY KEY(idDept));')

    import csv
    # Now import csv file content
    f = open(file_pop_csv, "rb")
    reader = csv.reader(f)

    # Populate table excluding first line (columns title)
    start = 0
    table_empty = table_isempty(cur, 'pop_dept')
    for idDept, nomDept, pop_2009_dept in reader:
        if start > 0 and table_empty:
            print idDept, nomDept, pop_2009_dept
            cur.execute('INSERT INTO pop_dept (idDept, nomDept, pop_2009_dept) VALUES (?,?,?)', (idDept.decode("utf-8"), nomDept.decode("utf-8"), pop_2009_dept.decode("utf-8")))
            #import ipdb; ipdb.set_trace()
        start += 1
    conn.commit()

    # Create new columns in main shp table
    try:
        cur.execute("ALTER TABLE " + tablename  + " ADD COLUMN pop2009 INTEGER")
        # Time to update main shp table
        cur.execute('UPDATE ' + tablename + ' SET pop2009 = (SELECT pop_2009_dept FROM pop_dept WHERE pop_dept.idDept = ' + tablename +'.code_dept)')
        # Add column and update it to get population density
        cur.execute("ALTER TABLE " + tablename  + " ADD COLUMN density2009 INTEGER")
        cur.execute('UPDATE ' + tablename + ' SET density2009 = "pop2009"/ (st_area("Geometry")/1000000)')
        conn.commit()
    except:
        print "Column already exist"
        pass # handle the error

