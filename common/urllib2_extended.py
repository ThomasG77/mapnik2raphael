#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
from StringIO import StringIO
import gzip

def urllibopenwithheaders(url, header = False):
    """
    Function to add headers to urllib2 or it fails for wikipedia (403 error)
    and some others sites. Header option is to see header status if value = True
    """
    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        req = urllib2.Request(url, headers={'User-Agent' : user_agent})
        page = urllib2.urlopen(req)
        headers = page.info()
        # Deal with gunzip content
        if headers.getheader("Content-Encoding") == 'gzip':
            buf = StringIO( page.read())
            page = gzip.GzipFile(fileobj=buf)
        if header: # Condition for headers
            #import ipdb; ipdb.set_trace()
            print headers
        content = page.read()
        return content
    except urllib2.HTTPError, e:
        print e.read()

