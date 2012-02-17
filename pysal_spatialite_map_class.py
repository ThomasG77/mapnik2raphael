#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)
cur = conn.cursor()

with closing(cur):
    cur.execute('SELECT ' + col_analyse + ' FROM "' + tablename + '"')

    values = []
    for series in cur.fetchall():
        #print series[0]
        values.append(series[0])

# For maps discretisation

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

def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]

quantile = [float(trunc(values[0], 2))]
last_value = float(trunc(upper_values[-1], 2)) + 10**-2
upper_values[-1] = last_value
quantile.extend([round(classes, 2) for classes in upper_values])

