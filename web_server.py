#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from spatialite_sqlite import *
from download_and_zip import *
from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
import json
import os

cur = conn.cursor()

with closing(cur):

    html = showquery(cur, 'SELECT code_dept, substr(upper(nom_dept),1,1) || substr(lower(nom_dept),-length(nom_dept)+1) as nom_dept_title, replace(replace(lower(nom_dept),"-",""),"\'","") as nom_dept_clean, description_wikipedia, svg FROM "departements"')

    def executecgi(cur):
        print "Content-Type: application/json\n"
        print showdata(cur)

    from bottle import route, run, static_file
    @route('/showdata')
    def showdata():
        cur.execute('''SELECT code_dept, substr(upper(nom_dept),1,1) ||
        substr(lower(nom_dept),-length(nom_dept)+1) as nom_dept_title,
        replace(replace(lower(nom_dept),"-",""),"\'","") as nom_dept_clean,
        description_wikipedia, svg FROM "departements"''')
        fieldnames = [name[0] for name in cur.description]
        #print fieldnames
        result = []
        for row in cur.fetchall():
            rowset = []
            for field in zip(fieldnames, row):
                rowset.append(field)
            result.append(dict(rowset))
            #cur.close()
        #print result
        return json.dumps(result)

    @route('/france.html')
    def france():
        return open('france.html', 'r')

    @route('/css/<filename:path>')
    def send_static(filename):
        return static_file(filename, root='./css/')

    @route('/js/<filename:path>')
    def send_static(filename):
        return static_file(filename, root='./js/')

    showdata()
    run(host='localhost', port=8000)

