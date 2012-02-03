#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
from download_and_zip import *

# Download mustache js
os.chdir("js")
f = download_file(url_mustache)

# Extract ZIP
extract(f, ".")

# Delete original file
os.remove(f)

# Get unzip dir name
mustachedirtoremove = glob.glob('*mustache*')

# Move mustache.js file
os.rename(os.path.join(mustachedirtoremove[0], "mustache.js"), "mustache.js")

# Delete dir now
shutil.rmtree(mustachedirtoremove[0])

os.chdir("..")

