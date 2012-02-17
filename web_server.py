#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
from spatialite_sqlite import *
from download_and_zip import *
import json
from pysal_spatialite_map_class import quantile

#print quantile

cur = conn.cursor()

with closing(cur):

    from bottle import route, run, static_file
    #@route('/raw_svg')
    @route('/raw_svg', method='POST')
    def showdata():
        cur.execute('''SELECT code_dept, substr(upper(nom_dept),1,1) ||
        substr(lower(nom_dept),-length(nom_dept)+1) as nom_dept_title,
        replace(replace(lower(nom_dept),"-",""),"\'","") as nom_dept_clean,
        svg FROM "departements"''')
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

    @route('/raw_svg_letters', method='POST')
    def showdataletters():
        cur.execute('SELECT path as svg, x, y FROM "letters"')
        fieldnames = [name[0] for name in cur.description]
        result = []
        for row in cur.fetchall():
            rowset = []
            for field in zip(fieldnames, row):
                rowset.append(field)
            result.append(dict(rowset))
        return json.dumps(result)
    @route('/attributes', method='POST')
    def showdataattributes():
        cur.execute('''SELECT substr(upper(nom_dept),1,1) ||
        substr(lower(nom_dept),-length(nom_dept)+1) as nom_dept_title,
        replace(replace(lower(nom_dept),"-",""),"\'","") as nom_dept_clean,
        density2009, description_wikipedia FROM "departements"''')
        fieldnames = [name[0] for name in cur.description]
        result = []
        for row in cur.fetchall():
            rowset = []
            for field in zip(fieldnames, row):
                rowset.append(field)
            result.append(dict(rowset))
        return json.dumps(result)
    @route('/classification', method='POST')
    def showclassification():
        return json.dumps({'classquantile': quantile})

    @route('/france.html')
    def france():
        return open('france.html', 'r')

    @route('/favicon.ico')
    def favicon():
        return static_file('favicon.ico', './')

    @route('/css/<filename:path>')
    def send_static(filename):
        return static_file(filename, root='./css/')

    @route('/js/<filename:path>')
    def send_static(filename):
        return static_file(filename, root='./js/')

    showdata()
    run(host='localhost', port=8000)

