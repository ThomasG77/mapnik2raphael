#!/usr/bin/env python

import cairo
from mapnik import Style, Rule, Color, Filter, LineSymbolizer, PolygonSymbolizer, TextSymbolizer, label_placement, SQLite, Layer, Map, render, Shapefile

# manage projection
proj4 = '+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'

map_output = 'france'
m = Map(300, 300, proj4)

m.background = Color('steelblue')
s = Style()
r = Rule()

r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'), 0.1))

t = TextSymbolizer('code_dept', 'DejaVu Sans Book', 8, Color('black'))
f = Filter("[code_dept]<>'75' and [code_dept]<>'92' and [code_dept]<>'93' and [code_dept]<>'94'")
t.allow_overlap = 1
t.label_placement = label_placement.POINT_PLACEMENT
s1 = Style()
r1 = Rule()
r1.symbols.append(t)
r1.filter = f
s1.rules.append(r1)
m.append_style('Text', s1)

s.rules.append(r)
m.append_style('My Style', s)

lyr = Layer('france', proj4)
import os
lyr.datasource = SQLite(base=os.getcwd(), file = 'france.sqlite', table = 'departements', geometry_field = 'Geometry', key_field = 'pkuid', extent = '99226.000000,6049647.000000,1242375.000000,7110524.000000', wkb_format = 'spatialite')

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
    surface.finish()

