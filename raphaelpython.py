#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Retrieve IGN departements file
import retrieve_file_france

# Import shp into spatialite and manage some structure
import shp_import_and_structure_departements

# Change database structure and retrieve content with web scrapping
import depts_wikipedia

# Retrieve pop 2009 from INSEE with web scrapping, write to CSV, import into database, join with spatial table departements
import scrapping_insee_pop_2009

# Import ino db and join
import import_csv_pop_dept_2009

# Calculate chloropleth class and do some histograms with matplotlib
import spatialite_map_class_intervals

# Generate SVG using Mapnik from spatialite database
import render_cairo_svg_france

# Download scour and unzip (a python standalone script to clean SVG)
import download_scour

# Download mustache and unzip (a js templating system)
import download_mustache_js

# Clean SVG path (No details but solve SVG path problems with Raphael JS)
import subprocess
subprocess.call(["python", "scour/scour.py", "-i", "france.svg", "-o", "france_scour.svg"])

# 2 ways to get SVG
# First, with raphaeljs and spatialite only
# SQL request for SVG comparing
# select length(asSVG("Geometry",0)) as svg_absolute, length(asSVG("Geometry",1)) as svg_relative, length(asSVG("Geometry",1, 0)) as svg_relative_precision0, length(asSVG(SimplifyPreserveTopology("Geometry", 100),1, 0)) as simplify from departements;
# UPDATE departements SET svg = asSVG("Geometry",1);
# FRANCE GEO EXTENT
# 99226 -7110524 1143149 1060877

# Make auto BBOX, img size and geographic or graphic coordinates data
#create ex (already exist in php with PostgreSQL)


# Parse svg to retrieve "good" SVG path for geometries and also to get vectorized text for labelling
import svg_parsing

# Download Raphael JS lib
import download_raphael

# Generate files for Raphael map final demo
import generateRaphaelResult

# TODO
# Manage wrong letters for Ile de France (exclude some "departements" to replace with "Ile de France") - Play at Mapnik level and with wkt
# Make a chloropleth map and retrieve color properties from generated SVG
# or generate class in db and affect color in db, so no svg  parsing for color
# Make auto BBOX, img size and geographic or graphic coordinates data using ogr / gdal
# Make a model compliant to deal with time (will create dependencies to a js framework/lib for managing timeline)
# Make no name appli (some constants like france or depts must be choose by user)
# Clean wikipedia description (wikipedia pages anchors)
# Change title in html template (prefecture name for the moment)
# Solve below
"""<sup>
  <a href="http://upload.wikimedia.orghttp://fr.wikipedia.org/wikipedia/commons/b/ba/Fr-Paris--Indre_%28d%C3%A9partement_de_l%E2%80%99%29.ogg">
   <img alt="Prononciation du titre dans sa version originale" src="http://upload.wikimedia.orghttp://fr.wikipedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/11px-Loudspeaker.svg.png" width="11" height="11" />
  </a>
 </sup>
"""
# Refactoring code to  a class sharing cur connexion with "init model"

# Need to play with js_svg_anim.js for letters (wrong for the moment : use only one source for template)
# OK, solved
# Animation on hover = responsible of letters disparition (supposed solution = kind of transparency)
# OK, change st.toFront() to st.toBack() in mouseout in file js_svg_anim.tmpl

