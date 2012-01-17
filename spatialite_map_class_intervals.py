#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pyspatialite import dbapi2 as sqlite
import variables_config # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
from contextlib import closing

tablename = variables_config.tablename
sqlitedatabase = variables_config.sqlitedatabase

conn = sqlite.connect(sqlitedatabase)
cur = conn.cursor()

with closing(cur):
    cur.execute("SELECT pop2009 FROM " + tablename)

    values = []
    for series in cur.fetchall():
        #print series[0]
        values.append(series[0])


from class_intervals import quantile, equal, pretty, std_dev, jenks

quantile, equal_interval, r_pretty, std_dev, jenks = quantile(values, 5), equal(values, 5), pretty(values, 5), std_dev(values, 5), jenks(values, classes=5)

print "Equal Interval: ", equal_interval, len(equal_interval) - 1
print "Quantile: ", quantile, len(quantile) - 1
print "Natural Breaks (Jenks): ", jenks, len(jenks) - 1
print "R's Pretty: ", r_pretty, len(r_pretty) - 1
print "Standard Deviation: ", std_dev, len(std_dev) - 1



# Sort values (useful only if classification function are not launched : they already do it)
values.sort()
#print values

import matplotlib.pyplot as plt
import numpy as np

#print quantile[:-1][1:]

def xBreakValue(classificationMethod, yValues):
    xvalues = []
    for limit in classificationMethod[:-1][1:]:
        for value in yValues:
            if limit < value:
                xvalues.append(values.index(value))
                break
    #print xvalues
    return xvalues, classificationMethod[:-1][1:]

#print xBreakValue(jenks, values)

def addVerticalLine(pltObj, x, ymin = 0, color = 'r'):
    axisMax = pltObj.axis()[3]
    #print axisMax
    pltObj.axvline(x = x, ymin = ymin/axisMax, linewidth=1, color = color)
    #import ipdb; ipdb.set_trace()

listMethods = [quantile, equal_interval, r_pretty, std_dev, jenks]
#listMethods = [quantile]
for method in listMethods:
    #import ipdb; ipdb.set_trace()
    plt.figure(listMethods.index(method))
    y = np.array(values)
    N = len( y )
    x = range( N )
    width = 1/1.5
    plt.bar( x, y, width)
    xseries, yseries = xBreakValue(method, values)
    for x, y in zip(xseries, yseries):
        addVerticalLine(plt, x, ymin = y, color = 'r')
    plt.savefig("fig" + str(listMethods.index(method)) + ".png", dpi=150, orientation='landscape', format="png")
    #xBreakValue(method, values)








# Start figure 1
plt.figure(6)
plt.hist(values,bins=20)
plt.savefig("fig6.png", dpi=150, orientation='landscape', format="png")
#plt.show()

