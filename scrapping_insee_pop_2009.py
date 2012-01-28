#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.urllib2_extended import *
from variables_config import * # Contains shared variables (See http://docs.python.org/faq/programming.html#how-do-i-share-global-variables-across-modules)

data_pop_2009_dept = urllibopenwithheaders(url_pop)
soup_pop_2009_dept = BeautifulSoup(data_pop_2009_dept)

table_pop_2009_dept = soup_pop_2009_dept.find("table",
    { "id" : "departements" })

import csv

f = open(file_pop_csv, "wb")
wr = csv.writer(f, quoting=csv.QUOTE_ALL)

#Write columns
wr.writerow(["idDept", "nomDept", "pop_2009_dept"])

values = []
for row in table_pop_2009_dept.findAll('tr')[1:]:
    cols = row.findAll('td')
    if len(cols) == 5 and cols[0].text != "" and len(cols[0].text) != 3:
        idDept, nomDept, pop_2009_dept = cols[0].text, cols[1].text, int(cols[2].text.replace(u"\xa0",""))
        values.append(pop_2009_dept)
        print idDept, nomDept, pop_2009_dept
        wr.writerow([idDept, nomDept.encode("utf-8"), pop_2009_dept])

f.close()

