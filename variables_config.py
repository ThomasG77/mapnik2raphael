#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Scour url (svg cleaner in python)
url_scour = "http://www.codedread.com/scour/scour-0.26.zip"

# Url to make scrapping for french population
url_pop = "http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/france-departements.asp"
file_pop_csv = "pop_france_depts_2009.txt"

# shp and spatialite parameters
data_url = "http://professionnels.ign.fr/DISPLAY/000/528/175/5281750/GEOFLADept_FR_Corse_AV_L93.zip"
tablename = "departements"
shpfile = "departement"
coding = "CP1252"
prj = "2154"
sqlitedatabase = "france.sqlite"

# List of pattern for file cleaning

patterns_list = ['*.pyc', 'departement.*', 'fig*.png', 'limite_departement.*', '*.zip', 'france.sqlite', 'pop_france_depts_2009.txt', '*.svg', '*.html', '*.index']

dirs_to_delete = ['scour']


# db import
from pyspatialite import dbapi2 as sqlite
# db connexion (automatically responsible of sqlite db creation)
conn = sqlite.connect(sqlitedatabase)

# For autoclosing db without close with keyword with
from contextlib import closing

# For matplotlib and diagrams drawing
import matplotlib.pyplot as plt
import numpy as np

# Common useful lib
import glob
import os
import re
import fnmatch

# To use beautifulsoup and urllib2
from BeautifulSoup import BeautifulSoup

