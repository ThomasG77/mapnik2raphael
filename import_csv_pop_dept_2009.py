#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# TODO : reorganise func below : duplicated from shp_import_and_structure_departements.py
def table_isempty(table):
    cur.execute('SELECT * FROM ' + table)
    data = cur.fetchone()
    if data is None:
        return True
    else:
        return False


from pyspatialite import dbapi2 as sqlite
import variables_config # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
import os
from contextlib import closing

tablename = variables_config.tablename
sqlitedatabase = variables_config.sqlitedatabase

conn = sqlite.connect(sqlitedatabase)
cur = conn.cursor()

with closing(cur):
    # Create table for importing csv
    cur.execute('CREATE TABLE IF NOT EXISTS pop_dept(idDept TEXT, nomDept TEXT, pop2009Dept INTEGER, PRIMARY KEY(idDept));')

    import csv
    # Now import csv file content
    f = open("pop_france_depts_2009.txt", "rb")
    reader = csv.reader(f)

    # Populate table excluding first line (columns title)
    start = 0
    table_empty = table_isempty('pop_dept')
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

