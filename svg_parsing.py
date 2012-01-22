#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
from lxml import etree
from contextlib import closing
cur = conn.cursor()

with closing(cur):
    svg = etree.parse("france_scour.svg")
    ns = {'svg': 'http://www.w3.org/2000/svg', 'g': 'http://www.w3.org/2000/svg', 'path': 'http://www.w3.org/2000/svg', 'defs': 'http://www.w3.org/2000/svg', 'symbol': 'http://www.w3.org/2000/svg', 'use': 'http://www.w3.org/2000/svg', 'xlink': 'http://www.w3.org/1999/xlink'}
    box = svg.xpath('/*/@viewBox', namespaces = ns) # Or svg.xpath('//svg:svg/@viewBox', namespaces = ns)
    print box[0]

    pathd = svg.xpath('//svg:svg/g:g/g:g/path:path/@d', namespaces = ns) # Or svg.xpath('//svg:g/g:path/@d', namespaces = ns)

    count = 0
    for d in pathd:
        print d
        count = count + 1
        print count
        query = "UPDATE departements SET svg = '" +d + "' WHERE pkuid=" + str(count)
        cur.execute(query)
        print query

    # Create a new sqlite table to deal with letters

    query = "CREATE TABLE letters (letter TEXT, path TEXT, x DECIMAL, y DECIMAL)"
    cur.execute(query)

    # Retrieve data to complete new table

    reusedglyphsid = svg.xpath('//svg:svg/g:g/g:g/g:g/use:use/@xlink:href', namespaces = ns)
    count = 0
    for i in reusedglyphsid:
        count = count + 1
        query = "INSERT INTO letters (letter) VALUES ('" + i[1:] + "')"
        print query
        cur.execute(query)

    reusedglyphsx = svg.xpath('//svg:svg/g:g/g:g/g:g/use:use/@x', namespaces = ns)
    count = 0
    for i in reusedglyphsx:
        count = count + 1
        query = "UPDATE letters SET x=" + i + " WHERE ROWID =" + str(count)
        print query
        cur.execute(query)

    reusedglyphsy = svg.xpath('//svg:svg/g:g/g:g/g:g/use:use/@y', namespaces = ns)
    count = 0
    for i in reusedglyphsy:
        count = count + 1
        query = "UPDATE letters SET y=" + i + " WHERE ROWID =" + str(count)
        print query
        cur.execute(query)


    pathglyphsid = svg.xpath('//svg:svg/defs:defs/symbol:symbol/@id', namespaces = ns)
    pathglyphs = svg.xpath('//svg:svg/defs:defs/symbol:symbol/path:path/@d', namespaces = ns)
    glyphspathid = dict(zip(pathglyphsid, pathglyphs))

    for k, v in glyphspathid.iteritems():
        #print k, v
        query = "UPDATE letters SET path='" + v + "' WHERE letter = '" + k + "'"
        cur.execute(query)
        print query


    conn.commit() # obligatoire ici puisque l'on veut modifier la table en insérant des données

