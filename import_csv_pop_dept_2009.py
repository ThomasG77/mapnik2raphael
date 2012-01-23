#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.spatialite_sqlite import *
from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
cur = conn.cursor()
import os
from contextlib import closing

with closing(cur):
    # Create table for importing csv
    cur.execute('CREATE TABLE IF NOT EXISTS pop_dept(idDept TEXT, nomDept TEXT, pop2009Dept INTEGER, PRIMARY KEY(idDept));')

    import csv
    # Now import csv file content
    f = open(file_pop_csv, "rb")
    reader = csv.reader(f)

    # Populate table excluding first line (columns title)
    start = 0
    table_empty = table_isempty(cur, 'pop_dept')
    for idDept, nomDept, pop2009Dept in reader:
        if start > 0 and table_empty:
            print idDept, nomDept, pop2009Dept
            cur.execute('INSERT INTO pop_dept (idDept, nomDept, pop2009Dept) VALUES (?,?,?)', (idDept.decode("utf-8"), nomDept.decode("utf-8"), pop2009Dept.decode("utf-8")))
            #import ipdb; ipdb.set_trace()
        start += 1
    conn.commit()

    # Create new columns in main shp table
    try:
        cur.execute("ALTER TABLE " + tablename  + " ADD COLUMN pop2009 INTEGER")
        # Time to update main shp table
        cur.execute('UPDATE ' + tablename + ' SET pop2009 = (SELECT pop2009Dept FROM pop_dept WHERE pop_dept.idDept = ' + tablename +'.code_dept)')
        conn.commit()
    except:
        print "Column already exist"
        pass # handle the error

