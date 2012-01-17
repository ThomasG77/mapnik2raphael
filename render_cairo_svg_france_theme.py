#!/usr/bin/env python

import cairo
from mapnik import Style, Rule, Color, Filter, LineSymbolizer, PolygonSymbolizer, TextSymbolizer, label_placement, SQLite, Layer, Map, render, Shapefile, Expression, save_map

# manage projection
proj4 = '+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'

map_output = 'france'
m = Map(300, 300, proj4)

m.background = Color('steelblue')

t = TextSymbolizer(Expression('[code_dept]'), 'DejaVu Sans Book', 8, Color('black'))

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

s = basic_chloropleth_class(s, "[pop2009] > 1600000", color = Color(255, 255, 0))
s = basic_chloropleth_class(s, "[pop2009] < 1600000", color = Color(255, 0, 0))

m.append_style('My Style', s)


lyr = Layer('france', proj4)
import os
lyr.datasource = SQLite(base=os.getcwd(), file = 'france.sqlite', table = 'departements', geometry_field = 'Geometry', key_field = 'pkuid', extent = '99226.000000,6049647.000000,1242375.000000,7110524.000000', wkb_format = 'spatialite')

"""
roads2_lyr = mapnik.Layer('Roads')
roads2_lyr.srs = "+proj=lcc +ellps=GRS80 +lat_0=49 +lon_0=-95 +lat+1=49 +lat_2=77 +datum=NAD83 +units=m +no_defs"
# Just get a copy from roads34_lyr
roads2_lyr.datasource = roads34_lyr.datasource

roads2_style_1 = mapnik.Style()
roads2_rule_1 = mapnik.Rule()
roads2_rule_1.filter = mapnik.Expression('[CLASS] = 2')
roads2_rule_stk_1 = mapnik.Stroke()
roads2_rule_stk_1.color = mapnik.Color(171,158,137)
roads2_rule_stk_1.line_cap = mapnik.line_cap.ROUND_CAP
roads2_rule_stk_1.width = 4.0
roads2_rule_1.symbols.append(mapnik.LineSymbolizer(roads2_rule_stk_1))
roads2_style_1.rules.append(roads2_rule_1)

m.append_style('road-border', roads2_style_1)

roads2_style_2 = mapnik.Style()
roads2_rule_2 = mapnik.Rule()
roads2_rule_2.filter = mapnik.Expression('[CLASS] = 2')
roads2_rule_stk_2 = mapnik.Stroke()
roads2_rule_stk_2.color = mapnik.Color(255,250,115)
"""

#lyr.datasource = Shapefile(file='departement')
lyr.styles.append('My Style')
lyr.styles.append('Text')

m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())
#m.zoom(.2)



file_formats = {'svg': cairo.SVGSurface,
                       }

for type_format in file_formats:
    print '// --  Rendering %s -----------------------------' % type_format
    file_open = open('%s.%s' % (map_output, type_format), 'w')
    surface = file_formats[type_format](file_open.name, m.width, m.height)
    render(m, surface)
    save_map(m,"tmp_map.xml")
    surface.finish()

