#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
from download_and_zip import * # generic module for downloading and unzipping files and dir

# Download ZIP

f = download_file(data_url)

# Extract ZIP
extract(f, ".")

# List files from zip to rename them to lowercase (spatialite and mapnik don't like upper case extension)
import zipfile
zip = zipfile.ZipFile(f)
namelist = zip.namelist()

for i in namelist:
    rename_case_all_os(i, option ="lower", extension_only = False)

