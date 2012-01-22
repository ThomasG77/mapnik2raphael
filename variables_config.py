#!/usr/bin/env python
# -*- coding: UTF-8 -*-

url_scour = "http://www.codedread.com/scour/scour-0.26.zip"

data_url = "http://professionnels.ign.fr/DISPLAY/000/528/175/5281750/GEOFLADept_FR_Corse_AV_L93.zip"
tablename = "departements"
shpfile = "departement"
coding = "CP1252"
prj = "2154"
sqlitedatabase = "france.sqlite"

# db import
from pyspatialite import dbapi2 as sqlite
# db connexion (automatically responsible of sqlite db creation)
conn = sqlite.connect(sqlitedatabase)

# For autoclosing db without close with keyword with
from contextlib import closing

# For matplotlib and diagrams drawing
import matplotlib.pyplot as plt
import numpy as np

import glob
import os
import re
import fnmatch

