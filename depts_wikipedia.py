#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

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

def describefrenchdepartement(url):
    """
    Function to retrieve simple description of the  metropolitan french
    departement wikipedia page.
    Depends from urllibopenwithheaders function
    """
    data_dept = urllibopenwithheaders(url)
    soup_dept = BeautifulSoup(data_dept)
    descriptif_dept = soup_dept.find("table",
        { "class" : "infobox_v2" }).findNext('p')
    return str(descriptif_dept).replace("/wiki", "http://fr.wikipedia.org/wiki")

import urllib2
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import gzip

from pyspatialite import dbapi2 as sqlite
import variables_config # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)

tablename = variables_config.tablename
sqlitedatabase = variables_config.sqlitedatabase

conn = sqlite.connect(sqlitedatabase)
cur = conn.cursor()

# Change structure for upcoming steps e.g. retrieve content from Wikipedia
# Included in a try except to deal when column are already created

try:
    cur.execute("ALTER TABLE " + tablename  + " ADD COLUMN svg TEXT")
    cur.execute("ALTER TABLE " + tablename  + " ADD COLUMN url_wikipedia TEXT")
    cur.execute("ALTER TABLE " + tablename  + " ADD COLUMN description_wikipedia TEXT")
    conn.commit()
except:
    print "It seems columns already exist"
    pass # handle the error

# Open URL
url_dept = 'http://fr.wikipedia.org/wiki/Département_français'
data = urllibopenwithheaders(url_dept)
soup = BeautifulSoup(data)
# Take the 4 columns with links to french departements
depts_list = soup.findAll('td', width="25%")
# Restrict to metropolitan departements
depts_metropole = depts_list[:3]

list_all = []
for i in depts_metropole:
    # Replace some text
    tmp =  str(i).replace('<td width="25%" valign="top">', "")
    tmp = tmp.replace('<td width="25%" valign="top" style="padding-left:5px">',
        "")
    tmp = tmp.replace('</td>', "<br />")
    tmp = tmp.replace("\n", "")
    list_all.append(tmp)

# Join columns text in one
intermediate_string = ''.join([str(x) for x in list_all])
# Remove last extra <br />
intermediate_string = rreplace(intermediate_string, "<br />", "", 1)

# Make an array from this unique string
intermediate_array = intermediate_string.split("<br />")

#print intermediate_array
for i in intermediate_array:
    code_dept = i[:2]
    url_page_dept = "http://fr.wikipedia.org" + i[12:].split('"', 1)[0]
    dept_description = describefrenchdepartement(url_page_dept)
    dept_description = BeautifulSoup(dept_description)
    #Clean some cites who use anchors
    cites = dept_description.findAll('sup', attrs={'id':'cite_ref-0'})
    [cite.extract() for cite in cites]
    print str(dept_description).decode("utf-8")
    print url_page_dept
    print code_dept
    cur.execute("UPDATE " + tablename +" SET url_wikipedia = (?), description_wikipedia = (?) WHERE CODE_DEPT = (?)", (url_page_dept, str(dept_description).decode("utf-8"), code_dept))
    conn.commit()
    print code_dept + ";" + url_page_dept

cur.close()

