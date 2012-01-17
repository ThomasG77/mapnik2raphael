#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

import urllib2
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import gzip

url = "http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/france-departements.asp"
data_pop_2009_dept = urllibopenwithheaders(url)
soup_pop_2009_dept = BeautifulSoup(data_pop_2009_dept)

table_pop_2009_dept = soup_pop_2009_dept.find("table",
    { "id" : "departements" })

import csv

f = open("pop_france_depts_2009.txt", "wb")
wr = csv.writer(f, quoting=csv.QUOTE_ALL)

#Write columns
wr.writerow(["idDept", "nomDept", "pop2009Dept"])

values = []
for row in table_pop_2009_dept.findAll('tr')[1:]:
    cols = row.findAll('td')
    if len(cols) == 5 and cols[0].text != "" and len(cols[0].text) != 3:
        idDept, nomDept, pop2009Dept = cols[0].text, cols[1].text, int(cols[2].text.replace(u"\xa0",""))
        values.append(pop2009Dept)
        print idDept, nomDept, pop2009Dept
        wr.writerow([idDept, nomDept.encode("utf-8"), pop2009Dept])

f.close()

