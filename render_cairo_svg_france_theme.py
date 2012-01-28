#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)

# get extent from shp (for mapnik)
from common.ogr_extent import *

# Retrieve extent and projection using gdal
shp_extent , proj4 = extent_and_proj(sqlitedatabase, sourcetype = 'SQLite')

import cairo
from mapnik import Style, Rule, Color, Filter, LineSymbolizer, PolygonSymbolizer, TextSymbolizer, label_placement, SQLite, Layer, Map, render, Shapefile, Expression, save_map

map_output = 'france'
m = Map(300, 300, proj4)

m.background = Color('steelblue')

t = TextSymbolizer(Expression('[code_dept]'), 'Linux Libertine O Regular', 8, Color('black'))

f = Expression("[code_dept]<>'75' and [code_dept]<>'92' and [code_dept]<>'93' and [code_dept]<>'94'")
t.allow_overlap = 1
t.label_placement = label_placement.POINT_PLACEMENT
s1 = Style()
r1 = Rule()
r1.symbols.append(t)
r1.filter = f
s1.rules.append(r1)
m.append_style('Text', s1)

s = Style()

def basic_chloropleth_class(s, def_filter, color = Color(255, 0, 0)):
    r = Rule()
    r.filter = Expression(def_filter)
    r.symbols.append(PolygonSymbolizer(color))
    s.rules.append(r)
    return s

"""
def simple_polygon_style(fill_color = "#f2eff9"):
    s = Style()
    r = Rule()
    r.symbols.append(PolygonSymbolizer(Color(fill_color)))
    r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'), 0.1))
    return s
"""

#m.append_style('My Style', simple_polygon_style())


#quantiletest = [77163.0, 246937.00000000006, 392518.00000000017, 605505.39999999991, 1072259.6000000003, 2571940]
#quantiletest = [14.922755846451, 932.89906405113561, 6374.9274822841471, 8928.8564733596268, 21208.385122261425]
quantiletest = [14.92, 46.57, 73.730000000000004, 121.47, 251.19, 932.89999999999998, 21208.389999999999]
length = len(quantiletest)

# Combine in list of list of 2 elements (min, max)
sequencepair = [quantiletest[index: index + 2:] for index, item in enumerate(quantiletest) if (index <= len(quantiletest) - 2)]
len_seq = len(sequencepair)

import colorbrewer
from color_brewer_test import *

color_obj = colorbrewer.OrRd[len_seq]

# Add color to get a list of list of 3 elements (min, max and RGB color list )
for index, seq  in enumerate(sequencepair):
    seq.append(color_obj[index])


# From classification and color, make layers
for index,seq in enumerate(sequencepair):
    if index == 0:
        exp = "[" + col_analyse + "] < " + str(seq[1]) + " and [" + col_analyse + "] >= " + str(seq[0])
    elif index == len_seq -1 :
        exp = "[" + col_analyse + "] <= " + str(seq[1]) + " and [" + col_analyse + "] > " + str(seq[0])
    else:
        exp = "[" + col_analyse + "] < " + str(seq[1]) + " and [" + col_analyse + "] > " + str(seq[0])
    s = basic_chloropleth_class(s, exp, color = Color(seq[2][0], seq[2][1], seq[2][2]))

m.append_style('My Style', s)

lyr = Layer('france', proj4)
import os
lyr.datasource = SQLite(base=os.getcwd(), file = sqlitedatabase, table = tablename, geometry_field = 'Geometry', key_field = 'pkuid', extent = shp_extent, wkb_format = 'spatialite')

lyr.styles.append('My Style')
lyr.styles.append('Text')

m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())



file_formats = {'svg': cairo.SVGSurface,
                       }

for type_format in file_formats:
    print '// --  Rendering %s -----------------------------' % type_format
    file_open = open('%s.%s' % (map_output, type_format), 'w')
    surface = file_formats[type_format](file_open.name, m.width, m.height)
    render(m, surface)
    save_map(m,"tmp_map.xml")
    surface.finish()

