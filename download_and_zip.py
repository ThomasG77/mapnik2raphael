#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
# Native libs solution
import urllib2
import shutil
import urlparse
import os

# Deal with header content when available
# See http://stackoverflow.com/questions/862173/how-to-download-a-file-using-python-in-a-smarter-way
def download_file(url, fileName=None):
    def getFileName(url,openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from it
            cd = dict(map(
                lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
                str(openUrl.info()).split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: return filename
        # if no filename was found above, parse it out of the final URL.
        return os.path.basename(urlparse.urlsplit(openUrl.url)[2])

    r = urllib2.urlopen(urllib2.Request(url))
    try:
        fileName = fileName or getFileName(url,r)
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(r,f)
        return fileName
    except:
        return None
    finally:
        r.close()
"""

# Requests module solution

import requests
import urlparse
import re

def download_file(url, fileName=None):
    def getFileName(url, req):
        h = req.headers
        if h.has_key("content-disposition") and h.get("content-disposition")!= None:
            if 'filename=' in h.get("content-disposition"):
                fileName = re.findall("filename=(\S+)", h.get("content-disposition"))[-1]
                fileName = fileName.strip("\"'")
        else:
            fileName = url.split("/")[-1]
        return fileName
    try:
        r = requests.get(url)
        #import ipdb; ipdb.set_trace()
        fileName = fileName or getFileName(url, r)
        with open(fileName, 'wb') as f:
            f.write(r.content)
        return fileName
    except:
        print "You got an error"
        pass

#download_file("http://www.nyaa.eu/?page=download&tid=280022")
#download_file("http://professionnels.ign.fr/DISPLAY/000/528/175/5281750/GEOFLADept_FR_Corse_AV_L93.zip")

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

