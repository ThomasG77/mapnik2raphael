#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def table_exists(cur, table):
    """Check a table exists"""
    if [] == cur.execute("PRAGMA table_info(%s)" % table).fetchall():
        return False
    else:
        return True

def table_isempty(cur, table):
    cur.execute('SELECT * FROM ' + table)
    data = cur.fetchone()
    if data is None:
        return True
    else:
        return False

"""Initializing Spatial MetaData
using v.2.4.0 this will automatically create
GEOMETRY_COLUMNS and SPATIAL_REF_SYS"""

def init_spatialdb(cur):
    """Check if sqlite database already contain spatialite functions. If not load them
    Depends from table_exists function
    """
    if table_exists(cur, 'spatial_ref_sys'):
        print "Spatial Database already initialized"
        return
    else:
        sql = 'SELECT InitSpatialMetadata()'
        cur.execute(sql)

def tableColumns(table, separator = ','):
    """Return table columns list with separator from a table
    """
    content = cur.execute("PRAGMA table_info(" + table + ")")
    tablenamelist = []
    for i in content:
        tablenamelist.append(i[1])
    print separator.join(tablenamelist)
    return separator.join(tablenamelist)

def tableStructureNoGeom(cur, inputtable, outputtable, epsgcode, typegeom, inputgeomcolumnname = "Geometry"):
    """
    Retrieve from a table his structure and and produce an SQL CREATE statement. For a spatial table, you can exclude geometry column
    """
    content = cur.execute("PRAGMA table_info(" + inputtable + ")")
    createString = "CREATE TABLE "
    createString = createString + outputtable
    createString = createString + "("
    listContent = []
    for i in content:
        row = i[1].lower() #column name
        if (i[2]!=""): #column type
            row = row + " " + i[2]
        if (i[5]==1): #primary key
            row = row + " PRIMARY KEY"
        else:
            if (i[3]==1): #not null
                row = row + " NOT NULL"
            if (str(i[4])!="None"): #default value
                row = row + " DEFAULT " + str(i[4])
        if (i[1]!= inputgeomcolumnname):
            listContent.append(row)
    createString = createString + ", ".join(listContent)
    createString = createString + ")"
    return str(createString)

def add_geom(table, epsgcode, typegeom):
    """Use Addgeometry on a table based on his name, his epsg code and his geometry type.
    """
    return "SELECT AddGeometryColumn('" + table  + "', 'Geometry', "\
                + epsgcode + ", '" + typegeom + "', 'XY');"

def import_shp(conn, table, absfilepath, encoding, epsgcode, typegeom):
    """Import shapefile into table using third method recommanded by spatialite dev http://groups.google.com/group/spatialite-users/msg/9ed3c66fca8f57ee
    We use an intermediate table to get shp structure before doing the true shp import.
    Depends from functions tableStructureNoGeom and tableColumns
    Derivated from http://pyod.googlecode.com/hg/fetcher.py?r=daed29f9bbadafb8ec8db12e8ff4401931184cef
    """
    global cur
    conn.isolation_level = 'DEFERRED'
    cur = conn.cursor()
    cur.execute("CREATE VIRTUAL TABLE tmp_shp_import USING VirtualShape('%s',%s,%s);" % (absfilepath, encoding, epsgcode)) # shp extension to lowercase
    create_no_geom = tableStructureNoGeom( cur, "tmp_shp_import", table, epsgcode, typegeom)
    print create_no_geom
    try:
        cur.execute(create_no_geom)
        add_geometry = add_geom(table, epsgcode, typegeom)
        cur.execute(add_geometry)
        structure = tableColumns("tmp_shp_import")
        cur.execute("INSERT INTO %s(%s) SELECT %s FROM tmp_shp_import;" % (table, structure.lower(), structure))
    except:
        print "Table already exists"
        pass
    cur.execute("DROP TABLE tmp_shp_import;")
    conn.commit()
    conn.isolation_level = None

def showquery(cur, request):
    cur.execute(request)
    fieldnames = [name[0] for name in cur.description]
    result = []
    for row in cur.fetchall():
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result

