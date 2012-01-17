#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def download_file(url, file_name):
    import urllib
    urllib.urlretrieve (url, file_name)

def extract(zipfilepath, extractiondir):
    """"Extract files and dir from zip from zipfilepath to extractiondir
    """
    import zipfile
    zip = zipfile.ZipFile(zipfilepath)
    zip.extractall(path=extractiondir)

def rename_case_all_os(name, option ="lower", extension_only = False):
    """"Rename a file and his extension to lower or upper case (name only, extension only or both)
    """
    import os
    try:
        os.rename(name, name + "tmp") # use a tmp name to deal with windows (rename lower to upper or upper to lower fail)
        if extension_only == True:
            extension = name.split('.')[1]
            basename = name.split('.')[0]
            if option == "lower": # lower case extension
                new_name = basename + "." + extension.lower()
            else: # upper case extension
                new_name = basename + "." + extension.upper()
            print "extension:" + new_name
            os.rename(name + "tmp", new_name)
        else:
            if option == "lower": # lower all name
                os.rename(name + "tmp", name.lower())
                print "name:" + name.lower()
            else: # upper all name
                os.rename(name + "tmp", name.upper())
                print "name:" + name.upper()
    except:
        print "File doesn't exist"
        pass

