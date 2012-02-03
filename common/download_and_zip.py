#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Requests module solution

import requests
import urlparse
import re

def download_file(url, fileName=None):
    def getFileName(url, req):
        h = req.headers
        file = None;
        if h.has_key("content-disposition") and h.get("content-disposition")!= None and 'filename=' in h.get("content-disposition"):
            file = re.findall("filename=(\S+)", h.get("content-disposition"))[-1]
            file = file.strip("\"'")
        else:
            file = url.split("/")[-1]
        return file
    try:
        r = requests.get(url)
        #import ipdb; ipdb.set_trace()
        fileName = getFileName(url, r)
        if fileName == None:
            print "You must set a fileName, unable to auto retrieve it"
        with open(fileName, 'wb') as f:
            f.write(r.content)
        return fileName
    except:
        print "You got an error"
        pass

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

