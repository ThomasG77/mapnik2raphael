#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
cur = conn.cursor()

with closing(cur):
    print tablename
    cur.execute('SELECT ' + col_analyse + ' FROM "' + tablename + '"')


    values = []
    for series in cur.fetchall():
        #print series[0]
        values.append(series[0])

#print values

# For maps discretisation


from class_intervals import quantile, equal, pretty, std_dev, jenks

class_number = 4
quantile, equal_interval, r_pretty, std_dev, jenks = quantile(values, class_number), equal(values, class_number), pretty(values, class_number), std_dev(values, class_number), jenks(values, classes=class_number)


print "Equal Interval: ", equal_interval, len(equal_interval) - 1
print "Quantile: ", quantile, len(quantile) - 1
print "Natural Breaks (Jenks): ", jenks, len(jenks) - 1
print "R's Pretty: ", r_pretty, len(r_pretty) - 1
print "Standard Deviation: ", std_dev, len(std_dev) - 1


import numpy as np
import pysal

# Sort values
values.sort()
x = np.array(values)

#import ipdb; ipdb.set_trace()




#intermediate_classification = pysal.esda.mapclassify.Quantiles(x, k = 4).bins
#intermediate_classification = pysal.esda.mapclassify.Fisher_Jenks(x, k = 4).bins
intermediate_classification = pysal.esda.mapclassify.Jenks_Caspall(x, k = 6).bins.tolist()

from decimal import *

getcontext().prec = 2
getcontext().rounding = ROUND_UP

upper_values = []
# Clean list
for classes in intermediate_classification:
    if isinstance(classes, list):
        upper_values.append(classes[0])
    elif isinstance(classes, str):
        upper_values.append(classes)
    else:
        print "You got en error"
        break

print upper_values




#ks = pysal.esda.mapclassify.K_classifiers(x)
"""
print ks.best.name
print ks.best.k
print ks.best.gadf

print ks.results
"""



def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]

quantile = [float(trunc(values[0], 2))]
last_value = float(trunc(upper_values[-1], 2)) + 10**-2
print last_value
upper_values[-1] = last_value
quantile.extend([round(classes, 2) for classes in upper_values])

print



print quantile


# Sort values (useful only if classification function are not launched : they already do it)
values.sort()
#print values

#print quantile[:-1][1:]


"""
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
"""

