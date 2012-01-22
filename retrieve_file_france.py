#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
from download_and_zip import * # generic module for downloading and unzipping files and dir

# Download ZIP
import urllib

file_name = data_url.split('/')[-1]
download_file(data_url, file_name)

# Extract ZIP
extract(file_name, ".")

# List files from zip to rename them to lowercase (spatialite and mapnik don't like upper case extension)
import zipfile
zip = zipfile.ZipFile(file_name)
namelist = zip.namelist()

for i in namelist:
    rename_case_all_os(i, option ="lower", extension_only = False)

# Function to delete files for testing purpose
def clean_depts():
    """"Clean files particular to samples (not generic)
    """
    import glob, os
    delete_file_list = glob.glob('departement.*')
    delete_file_list.extend(glob.glob('limite_departement.*'))
    delete_file_list.append(file_name)
    for filelist in delete_file_list:
        print os.path.join(os.getcwd(), filelist)
        os.remove(os.path.join(os.getcwd(), filelist))

# clean_depts() #optionnal to clean files

